from fastapi import Depends, File, UploadFile

from r2r.base import ChunkingConfig
from r2r.main.api.routes.ingestion.requests import (
    R2RIngestFilesRequest,
    R2RUpdateFilesRequest,
)

from ....assembly.factory import R2RProviderFactory
from ....engine import R2REngine
from ....services.ingestion_service import IngestionService
from ..base_router import BaseRouter


class IngestionRouter(BaseRouter):
    def __init__(self, engine: R2REngine):
        super().__init__(engine)
        self.setup_routes()

    def setup_routes(self):
        @self.router.post("/ingest_files")
        @self.base_endpoint
        async def ingest_files_app(
            files: list[UploadFile] = File(...),
            request: R2RIngestFilesRequest = Depends(
                IngestionService.parse_ingest_files_form_data
            ),
            auth_user=(
                Depends(self.engine.providers.auth.auth_wrapper)
                if self.engine.providers.auth
                else None
            ),
        ):
            chunking_config_override = None
            if request.chunking_config_override:
                config = ChunkingConfig(**request.chunking_config_override)
                chunking_config_override = (
                    R2RProviderFactory.create_chunking_provider(config)
                )

            return await self.engine.aingest_files(
                files=files,
                metadatas=request.metadatas,
                document_ids=request.document_ids,
                versions=request.versions,
                user=auth_user,
                chunking_config_override=chunking_config_override,
            )

        @self.router.post("/update_files")
        @self.base_endpoint
        async def update_files_app(
            files: list[UploadFile] = File(...),
            request: R2RUpdateFilesRequest = Depends(
                IngestionService.parse_update_files_form_data
            ),
            auth_user=(
                Depends(self.engine.providers.auth.auth_wrapper)
                if self.engine.providers.auth
                else None
            ),
        ):
            chunking_config_override = None
            if request.chunking_config_override:
                config = ChunkingConfig(**request.chunking_config_override)
                chunking_config_override = (
                    R2RProviderFactory.create_chunking_provider(config)
                )

            return await self.engine.aupdate_files(
                files=files,
                metadatas=request.metadatas,
                document_ids=request.document_ids,
                user=auth_user,
            )
