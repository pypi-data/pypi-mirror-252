// Copyright (C) 2021 Bosutech XXI S.L.
//
// nucliadb is offered under the AGPL v3.0 and as commercial software.
// For commercial licensing, contact us at info@nuclia.com.
//
// AGPL:
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.
//

use std::sync::Arc;

use nucliadb_core::protos::node_writer_server::NodeWriter;
use nucliadb_core::protos::{
    garbage_collector_response, op_status, EmptyQuery, GarbageCollectorResponse, NewShardRequest,
    NewVectorSetRequest, NodeMetadata, OpStatus, Resource, ResourceId, ShardCleaned, ShardCreated,
    ShardId, ShardIds, VectorSetId, VectorSetList,
};
use nucliadb_core::tracing::{self, Span, *};
use nucliadb_core::{Channel, NodeResult};
use tokio::sync::mpsc::UnboundedSender;
use tonic::{Request, Response, Status};

use crate::analytics::payload::AnalyticsEvent;
use crate::analytics::sync::send_analytics_event;
use crate::settings::Settings;
use crate::shards::errors::ShardNotFoundError;
use crate::shards::metadata::ShardMetadata;
use crate::shards::providers::unbounded_cache::UnboundedShardWriterCache;
use crate::shards::writer::ShardWriter;
use crate::telemetry::run_with_telemetry;
use crate::utils::list_shards;

pub struct NodeWriterGRPCDriver {
    shards: Arc<UnboundedShardWriterCache>,
    sender: Option<UnboundedSender<NodeWriterEvent>>,
    settings: Settings,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum NodeWriterEvent {
    ShardCreation,
    ShardDeletion,
}

impl NodeWriterGRPCDriver {
    pub fn new(settings: Settings, shard_cache: Arc<UnboundedShardWriterCache>) -> Self {
        Self {
            settings,
            shards: shard_cache,
            sender: None,
        }
    }

    /// This function must be called before using this service
    pub async fn initialize(&self) -> NodeResult<()> {
        if !self.settings.lazy_loading() {
            // If lazy loading is disabled, load
            let shards = Arc::clone(&self.shards);
            tokio::task::spawn_blocking(move || shards.load_all()).await??
        }
        Ok(())
    }

    pub fn with_sender(self, sender: UnboundedSender<NodeWriterEvent>) -> Self {
        Self {
            sender: Some(sender),
            ..self
        }
    }

    #[tracing::instrument(skip_all)]
    fn emit_event(&self, event: NodeWriterEvent) {
        if let Some(sender) = &self.sender {
            let _ = sender.send(event);
        }
    }
}

fn obtain_shard(
    shards: Arc<UnboundedShardWriterCache>,
    id: impl Into<String>,
) -> Result<Arc<ShardWriter>, tonic::Status> {
    let id = id.into();
    if let Some(shard) = shards.get(id.clone()) {
        return Ok(shard);
    }
    let id_clone = id.clone();
    let shards = shards.clone();
    let shard = shards.load(id_clone).map_err(|error| {
        if error.is::<ShardNotFoundError>() {
            tonic::Status::not_found(error.to_string())
        } else {
            tonic::Status::internal(format!("Error lazy loading shard {id}: {error:?}"))
        }
    })?;
    Ok(shard)
}

#[tonic::async_trait]
impl NodeWriter for NodeWriterGRPCDriver {
    async fn new_shard(
        &self,
        request: Request<NewShardRequest>,
    ) -> Result<Response<ShardCreated>, Status> {
        send_analytics_event(AnalyticsEvent::Create).await;
        let request = request.into_inner();
        let kbid = request.kbid.clone();
        let shard_id = uuid::Uuid::new_v4().to_string();
        let metadata = ShardMetadata::new(
            self.shards.shards_path.join(shard_id.clone()),
            shard_id,
            Some(kbid),
            request.similarity().into(),
            Some(Channel::from(request.release_channel)),
        );

        let shards = Arc::clone(&self.shards);
        let new_shard = tokio::task::spawn_blocking(move || shards.create(metadata))
            .await
            .map_err(|error| tonic::Status::internal(format!("Error creating shard: {error:?}")))?;

        match new_shard {
            Ok(new_shard) => {
                self.emit_event(NodeWriterEvent::ShardCreation);
                Ok(tonic::Response::new(ShardCreated {
                    id: new_shard.id.clone(),
                    document_service: new_shard.document_version() as i32,
                    paragraph_service: new_shard.paragraph_version() as i32,
                    vector_service: new_shard.vector_version() as i32,
                    relation_service: new_shard.relation_version() as i32,
                }))
            }
            Err(error) => Err(tonic::Status::internal(error.to_string())),
        }
    }

    async fn delete_shard(&self, request: Request<ShardId>) -> Result<Response<ShardId>, Status> {
        send_analytics_event(AnalyticsEvent::Delete).await;
        // Deletion does not require for the shard to be loaded.
        let shard_id = request.into_inner();

        let shards = Arc::clone(&self.shards);
        let shard_id_clone = shard_id.id.clone();
        let deleted = tokio::task::spawn_blocking(move || shards.delete(shard_id_clone))
            .await
            .map_err(|error| {
                tonic::Status::internal(format!("Error deleted shard {}: {error:?}", shard_id.id))
            })?;

        match deleted {
            Ok(_) => {
                self.emit_event(NodeWriterEvent::ShardDeletion);
                Ok(tonic::Response::new(shard_id))
            }
            Err(e) => {
                let error_msg = format!("Error deleting shard {:?}: {}", shard_id, e);
                error!("{}", error_msg);
                Err(tonic::Status::internal(error_msg))
            }
        }
    }

    async fn clean_and_upgrade_shard(
        &self,
        request: Request<ShardId>,
    ) -> Result<Response<ShardCleaned>, Status> {
        let shard_id = request.into_inner().id;

        // No need to load shard to upgrade it
        let shards = Arc::clone(&self.shards);
        let shard_id_clone = shard_id.clone();
        let upgraded = tokio::task::spawn_blocking(move || shards.upgrade(shard_id_clone))
            .await
            .map_err(|error| {
                tonic::Status::internal(format!("Error deleted shard {}: {error:?}", shard_id))
            })?;

        match upgraded {
            Ok(upgrade_details) => Ok(tonic::Response::new(upgrade_details)),
            Err(error) => Err(tonic::Status::internal(error.to_string())),
        }
    }

    async fn list_shards(
        &self,
        _request: Request<EmptyQuery>,
    ) -> Result<Response<ShardIds>, Status> {
        let shard_ids = list_shards(self.shards.shards_path.clone())
            .await
            .into_iter()
            .map(|id| ShardId { id })
            .collect();

        Ok(tonic::Response::new(ShardIds { ids: shard_ids }))
    }

    // Incremental call that can be call multiple times for the same resource
    async fn set_resource(&self, request: Request<Resource>) -> Result<Response<OpStatus>, Status> {
        let span = Span::current();
        let resource = request.into_inner();
        let shard_id = resource.shard_id.clone();
        let shards = Arc::clone(&self.shards);
        let shard_id_clone = shard_id.clone();
        let info = info_span!(parent: &span, "set resource");
        let write_task = || {
            run_with_telemetry(info, move || {
                let shard = obtain_shard(shards, shard_id_clone)?;
                shard
                    .set_resource(&resource)
                    .and_then(|()| shard.get_opstatus())
            })
        };
        let status = tokio::task::spawn_blocking(write_task)
            .await
            .map_err(|error| {
                tonic::Status::internal(format!("Blocking task panicked: {error:?}"))
            })?;
        match status {
            Ok(mut status) => {
                status.status = 0;
                status.detail = "Success!".to_string();
                Ok(tonic::Response::new(status))
            }
            Err(error) => {
                let status = OpStatus {
                    status: op_status::Status::Error as i32,
                    detail: error.to_string(),
                    field_count: 0_u64,
                    shard_id,
                    ..Default::default()
                };
                Ok(tonic::Response::new(status))
            }
        }
    }

    async fn remove_resource(
        &self,
        request: Request<ResourceId>,
    ) -> Result<Response<OpStatus>, Status> {
        let span = Span::current();
        let resource = request.into_inner();
        let shard_id = resource.shard_id.clone();
        let shards = Arc::clone(&self.shards);
        let shard_id_clone = shard_id.clone();
        let info = info_span!(parent: &span, "remove resource");
        let write_task = || {
            run_with_telemetry(info, move || {
                let shard = obtain_shard(shards, shard_id_clone)?;
                shard
                    .remove_resource(&resource)
                    .and_then(|()| shard.get_opstatus())
            })
        };
        let status = tokio::task::spawn_blocking(write_task)
            .await
            .map_err(|error| {
                tonic::Status::internal(format!("Blocking task panicked: {error:?}"))
            })?;
        match status {
            Ok(mut status) => {
                status.status = 0;
                status.detail = "Success!".to_string();
                Ok(tonic::Response::new(status))
            }
            Err(error) => {
                let status = OpStatus {
                    status: op_status::Status::Error as i32,
                    detail: error.to_string(),
                    field_count: 0_u64,
                    shard_id,
                    ..Default::default()
                };
                Ok(tonic::Response::new(status))
            }
        }
    }

    async fn add_vector_set(
        &self,
        request: Request<NewVectorSetRequest>,
    ) -> Result<Response<OpStatus>, Status> {
        let span = Span::current();
        let request = request.into_inner();
        let vectorset_id = match request.id {
            Some(ref vectorset_id) => vectorset_id.clone(),
            None => {
                return Err(tonic::Status::invalid_argument(
                    "Vectorset ID must be provided",
                ))
            }
        };
        let shard_id = match vectorset_id.shard {
            Some(ref shard_id) => &shard_id.id,
            None => return Err(tonic::Status::invalid_argument("Shard ID must be provided")),
        };

        let shards = Arc::clone(&self.shards);
        let shard_id_clone = shard_id.clone();
        let info = info_span!(parent: &span, "add vector set");
        let task = || {
            run_with_telemetry(info, move || {
                let shard = obtain_shard(shards, shard_id_clone)?;
                shard
                    .add_vectorset(&vectorset_id, request.similarity())
                    .and_then(|()| shard.get_opstatus())
            })
        };
        let status = tokio::task::spawn_blocking(task).await.map_err(|error| {
            tonic::Status::internal(format!("Blocking task panicked: {error:?}"))
        })?;
        match status {
            Ok(mut status) => {
                status.status = 0;
                status.detail = "Success!".to_string();
                Ok(tonic::Response::new(status))
            }
            Err(error) => Err(tonic::Status::internal(error.to_string())),
        }
    }

    async fn remove_vector_set(
        &self,
        request: Request<VectorSetId>,
    ) -> Result<Response<OpStatus>, Status> {
        let span = Span::current();
        let request = request.into_inner();
        let shard_id = match request.shard {
            Some(ref shard_id) => &shard_id.id,
            None => return Err(tonic::Status::invalid_argument("Shard ID must be provided")),
        };
        let shards = Arc::clone(&self.shards);
        let shard_id_clone = shard_id.clone();
        let info = info_span!(parent: &span, "remove vector set");
        let task = || {
            run_with_telemetry(info, move || {
                let shard = obtain_shard(shards, shard_id_clone)?;
                shard
                    .remove_vectorset(&request)
                    .and_then(|()| shard.get_opstatus())
            })
        };
        let status = tokio::task::spawn_blocking(task).await.map_err(|error| {
            tonic::Status::internal(format!("Blocking task panicked: {error:?}"))
        })?;
        match status {
            Ok(mut status) => {
                status.status = 0;
                status.detail = "Success!".to_string();
                Ok(tonic::Response::new(status))
            }
            Err(error) => Err(tonic::Status::internal(error.to_string())),
        }
    }

    async fn list_vector_sets(
        &self,
        request: Request<ShardId>,
    ) -> Result<Response<VectorSetList>, Status> {
        let span = Span::current();
        let shard_id = request.into_inner();
        let shards = Arc::clone(&self.shards);
        let shard_id_clone = shard_id.id.clone();
        let info = info_span!(parent: &span, "list vector sets");
        let task = || {
            let shard = obtain_shard(shards, shard_id_clone)?;
            run_with_telemetry(info, move || shard.list_vectorsets())
        };
        let status = tokio::task::spawn_blocking(task).await.map_err(|error| {
            tonic::Status::internal(format!("Blocking task panicked: {error:?}"))
        })?;
        match status {
            Ok(vectorset) => {
                let list = VectorSetList {
                    vectorset,
                    shard: Some(shard_id),
                };
                Ok(tonic::Response::new(list))
            }
            Err(error) => Err(tonic::Status::internal(error.to_string())),
        }
    }

    async fn get_metadata(
        &self,
        _request: Request<EmptyQuery>,
    ) -> Result<Response<NodeMetadata>, Status> {
        let metadata_settings = self.settings.clone();
        let metadata = crate::node_metadata::NodeMetadata::new(metadata_settings).await;
        match metadata {
            Ok(metadata) => Ok(tonic::Response::new(metadata.into())),
            Err(error) => Err(tonic::Status::internal(error.to_string())),
        }
    }

    async fn gc(
        &self,
        request: Request<ShardId>,
    ) -> Result<Response<GarbageCollectorResponse>, Status> {
        send_analytics_event(AnalyticsEvent::GarbageCollect).await;
        let shard_id = request.into_inner();
        let shards = Arc::clone(&self.shards);
        let shard_id_clone = shard_id.id.clone();
        let span = Span::current();
        let info = info_span!(parent: &span, "list vector sets");
        let task = || {
            let shard = obtain_shard(shards, shard_id_clone)?;
            run_with_telemetry(info, move || shard.gc())
        };
        let result = tokio::task::spawn_blocking(task).await.map_err(|error| {
            tonic::Status::internal(format!("Blocking task panicked: {error:?}"))
        })?;
        match result {
            Ok(status) => Ok(tonic::Response::new(GarbageCollectorResponse {
                status: garbage_collector_response::Status::from(status) as i32,
            })),
            Err(error) => Err(tonic::Status::internal(error.to_string())),
        }
    }
}
