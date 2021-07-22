FROM tiangolo/uvicorn-gunicorn:python3.8

ENV CURL_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt

RUN git clone https://github.com/stac-utils/stac-fastapi\
    && pip install -e stac-fastapi/stac_fastapi/api \
    && pip install -e stac-fastapi/stac_fastapi/types \
    && pip install -e stac-fastapi/stac_fastapi/extensions \
    && pip install -e stac-fastapi/stac_fastapi/sqlalchemy \
    && pip install -e stac-fastapi/stac_fastapi/pgstac

COPY stac_fastapi/ /tmp/stac_fastapi/
RUN pip install /tmp/stac_fastapi/rio_stac["sqlalchemy,pgstac"] --no-cache-dir

RUN rm -rf /tmp/stac_fastapi

COPY demo demo/
