"""demo for pgstac."""

from stac_fastapi.pgstac.app import api
from stac_fastapi.rio_stac.pgstac import RioStacPGStac

extension = RioStacPGStac()
extension.register(api.app)

app = api.app
