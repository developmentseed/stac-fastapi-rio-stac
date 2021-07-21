"""rio_stac extension."""

import datetime
from typing import Any, Coroutine, Dict, List, Optional

import pystac
from pydantic import BaseModel, Field, validator
from rio_stac.stac import create_stac_item
from starlette.concurrency import run_in_threadpool


class CreateItemModel(BaseModel):
    """Items model."""

    source: str
    id: Optional[str]
    input_datetime: Optional[str] = Field(
        default=datetime.datetime.utcnow(), alias="datetime"
    )
    extensions: Optional[List[str]]
    properties: Optional[Dict[str, Any]]
    assets: Optional[Dict[str, Any]]
    asset_name: str = "asset"
    asset_roles: Optional[List[str]]
    asset_media_type: Optional[str] = "auto"
    asset_href: Optional[str]
    with_proj: bool = False
    with_raster: bool = False
    raster_max_size: int = 1024

    @validator("asset_media_type")
    def return_pystac_mediatype(cls, v):
        """return mediatype."""
        if v and v != "auto":
            return pystac.MediaType[v].value
        return v

    # TODO: add datetime validation
    # @validator("datetime")
    # def validate_datetime(cls, v):
    #     if v and v != "auto":
    #         return pystac.MediaType[v].value
    #     return v
    # if not input_datetime:
    #     input_datetime = datetime.datetime.utcnow()
    # else:
    #     if "/" in input_datetime:
    #         start_datetime, end_datetime = input_datetime.split("/")
    #         property["start_datetime"] = datetime_to_str(
    #             str_to_datetime(start_datetime)
    #         )
    #         property["end_datetime"] = datetime_to_str(str_to_datetime(end_datetime))
    #         input_datetime = None
    #     else:
    #         input_datetime = str_to_datetime(input_datetime)

    def create_item(self, **kwargs) -> pystac.Item:
        """create STAC item from input."""
        return create_stac_item(**self.dict(exclude_none=True), **kwargs)

    async def acreate_item(self, **kwargs) -> Coroutine[Any, Any, pystac.Item]:
        """create STAC item from input but ASYNC."""
        return await run_in_threadpool(
            create_stac_item(**self.dict(exclude_none=True), **kwargs)
        )
