"""rio_stac extension."""

import datetime
from typing import Any, Coroutine, Dict, List, Optional

import pystac
from pydantic import BaseModel, Field, root_validator, validator
from pystac.utils import datetime_to_str, str_to_datetime
from rio_stac.stac import create_stac_item
from starlette.concurrency import run_in_threadpool


class CreateItemModel(BaseModel):
    """Items model."""

    source: str
    id: Optional[str]
    input_datetime: Optional[datetime.datetime] = Field(
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

    @root_validator(pre=True)
    def validate_datetime(cls, values):
        """validate datetime."""
        if "datetime" in values:
            indate = values.pop("datetime")
            if "/" in indate:
                props = values.pop("properties", {})
                start_datetime, end_datetime = indate.split("/")
                props["start_datetime"] = datetime_to_str(
                    str_to_datetime(start_datetime)
                )
                props["end_datetime"] = datetime_to_str(str_to_datetime(end_datetime))
                values["properties"] = props
                values["datetime"] = None
            else:
                values["datetime"] = str_to_datetime(indate)

        return values

    def create_item(self, **kwargs) -> pystac.Item:
        """create STAC item from input."""
        return create_stac_item(**self.dict(exclude_none=True), **kwargs)

    async def acreate_item(self, **kwargs) -> Coroutine[Any, Any, pystac.Item]:
        """create STAC item from input but ASYNC."""
        return await run_in_threadpool(
            create_stac_item, **self.dict(exclude_none=True), **kwargs
        )
