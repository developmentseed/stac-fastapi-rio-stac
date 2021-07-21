FROM tiangolo/uvicorn-gunicorn:python3.8

ENV CURL_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt

COPY src/stac_fastapi/ /tmp/stac_fastapi/
RUN pip install /tmp/stac_fastapi/rio_stac[sqlachemy,pgstac] --no-cache-dir

RUN rm -rf /tmp/stac_fastapi

COPY demo demo/
