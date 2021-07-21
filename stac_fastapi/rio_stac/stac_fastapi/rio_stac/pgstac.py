"""rio-stac extension for pgstac."""

import attr
from fastapi import APIRouter, FastAPI, Path
from stac_pydantic import Item
from starlette.requests import Request

from stac_fastapi.pgstac.db import dbfunc
from stac_fastapi.rio_stac.models import CreateItemModel
from stac_fastapi.types.extension import ApiExtension

router = APIRouter()


@attr.s
class RioStacPGStac(ApiExtension):
    """Rio-stac extension for PGSTAC."""

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
            response_model=Item,
            response_model_exclude_none=True,
            response_model_exclude_unset=True,
        )
        async def create_and_add_item(
            request: Request,
            body: CreateItemModel,
            collectionId: str = Path(..., description="Collection ID"),
        ) -> Item:
            """Create and Insert Item."""
            pool = request.app.state.writepool

            pystac_item = await body.acreate_item(
                collection=collectionId,
                collection_url=f"{request.base_url}/collections/{collectionId}",
            )
            item = Item(**pystac_item)
            await dbfunc(pool, "create_item", item)
            return item

        app.include_router(router, tags=["rio-stac Extension"])
