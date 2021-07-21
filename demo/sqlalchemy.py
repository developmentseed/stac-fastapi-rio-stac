"""demo for sqlachemy."""

from stac_fastapi.rio_stac.sqlalchemy import RioStacSqlalchemy
from stac_fastapi.sqlalchemy.app import api, session

extension = RioStacSqlalchemy(session)
extension.register(api.app)

app = api.app
