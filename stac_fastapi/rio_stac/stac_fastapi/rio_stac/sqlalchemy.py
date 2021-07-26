"""rio-stac extension for sqlalchemy."""

import json

import attr
from fastapi import APIRouter, FastAPI, Path
from starlette.requests import Request

from stac_fastapi.rio_stac.models import CreateItemModel
from stac_fastapi.sqlalchemy.models import database, schemas
from stac_fastapi.sqlalchemy.session import Session
from stac_fastapi.types.extension import ApiExtension

router = APIRouter()


@attr.s
class RioStacSqlalchemy(ApiExtension):
    """Rio-stac extension for SQLAlchemy."""

    session: Session = attr.ib(default=attr.Factory(Session.create_from_env))

    def __attrs_post_init__(self):
        """Create sqlalchemy engine."""
        self.engine = self.session.writer.cached_engine

    def register(self, app: FastAPI) -> None:
        """Register the extension with a FastAPI application.

        Args:
            app: target FastAPI application.

        Returns:
            None
        """
        router = APIRouter()

        @router.post(
            "/collections/{collectionId}/add",
            response_model=None,
            response_model_exclude_none=True,
            response_model_exclude_unset=True,
        )
        def create_and_add_item(
            request: Request,
            body: CreateItemModel,
            collectionId: str = Path(..., description="Collection ID"),
        ) -> schemas.Item:
            """Create and Insert Item."""
            item = schemas.Item(
                **body.create_item(
                    collection=collectionId,
                    collection_url=f"{request.base_url}/collections/{collectionId}",
                ).to_dict()
            )

            item = item.dict(exclude_none=True)
            item["geometry"] = json.dumps(item["geometry"])
            item["collection_id"] = item.pop("collection")
            item["datetime"] = item["properties"].pop("datetime")

            data = database.Item.from_schema(item)
            with self.session.writer.context_session() as session:
                session.add(data)
                data.base_url = str(request.base_url)
                return schemas.Item.from_orm(data)

        app.include_router(router, tags=["rio-stac Extension"])
