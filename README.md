## stac-fastapi-rio-stac

stac-fastapi extension which adds a `/collections/{collectionId}/create` to a stac-fastapi application to create STAC items from a raster dataset url.

This extension use [rio-stac](https://developmentseed.org/rio-stac/) to create a valid STAC Item.

![](https://user-images.githubusercontent.com/10407788/126988918-a98df987-6a8a-4367-aeae-1f0d1e1ca8a2.png)


## How To

```python
"""stac_fastapi pgstac application with rio-stac extension."""
from stac_fastapi.pgstac.app import api
from stac_fastapi.rio_stac.pgstac import RioStacPGStac

# Register to the rio-stac extension to the api
extension = RioStacPGStac()
extension.register(api.app)

# $ uvicorn myfilec:app --reload --port 8082 --host 0.0.0.0
app = api.app
```

```python
import requests

endpoint = "http://0.0.0.0:8082"

body = dict(
    source="https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/34/S/GA/2020/3/S2A_34SGA_20200318_0_L2A/TCI.tif",
    id="S2A_34SGA_20200318_0_L2A",
    datetime="2020-03-28T00:00:00",
    asset_name="TCI",
    asset_media_type="COG",
    with_proj=True,
    with_raster=True,
)

r = requests.post(f"{endpoint}/collections/test/add", json=body)
```
