"""tests rio-stac models."""

import os

import pytest

from stac_fastapi.rio_stac.models import CreateItemModel

PREFIX = os.path.join(os.path.dirname(__file__), "fixtures")


def test_create_items_model():
    """Create item from input model."""

    input_model = CreateItemModel(
        source=os.path.join(PREFIX, "cog.tif"), id="cog", asset_media_type="auto"
    )
    assert input_model.input_datetime
    assert input_model.asset_media_type == "auto"

    input_model = CreateItemModel(
        source=os.path.join(PREFIX, "cog.tif"), id="cog", asset_media_type="COG"
    )
    assert input_model.input_datetime
    assert (
        input_model.asset_media_type
        == "image/tiff; application=geotiff; profile=cloud-optimized"
    )

    itm = input_model.create_item().to_dict()
    assert itm["stac_version"]
    assert itm["id"] == "cog"
    assert itm["properties"]["datetime"]
    assert itm["geometry"]
    assert itm["assets"]["asset"]
    assert itm["stac_extensions"] == []


def test_create_items_model_datetime():
    """Create item from input model."""

    input_model = CreateItemModel(
        source=os.path.join(PREFIX, "cog.tif"), id="cog", datetime="2010-01-01",
    )
    itm = input_model.create_item().to_dict()
    assert itm["properties"]["datetime"] == "2010-01-01T00:00:00Z"

    input_model = CreateItemModel(
        source=os.path.join(PREFIX, "cog.tif"),
        id="cog",
        datetime="2010-01-01/2010-01-02",
    )
    assert not input_model.input_datetime
    itm = input_model.create_item().to_dict()
    assert not itm["properties"]["datetime"]
    assert itm["properties"]["start_datetime"] == "2010-01-01T00:00:00Z"
    assert itm["properties"]["end_datetime"] == "2010-01-02T00:00:00Z"


@pytest.mark.asyncio
async def test_acreate_item():
    """Create item from input model."""
    input_model = CreateItemModel(
        source=os.path.join(PREFIX, "cog.tif"), id="cog", asset_media_type="COG"
    )
    itm = await input_model.acreate_item()
    item = itm.to_dict()
    assert item["stac_version"]
    assert item["id"] == "cog"
    assert item["properties"]["datetime"]
    assert item["geometry"]
    assert item["assets"]["asset"]
    assert item["stac_extensions"] == []
