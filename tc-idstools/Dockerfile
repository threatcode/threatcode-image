

FROM ghcr.io/threatcode/python:3-alpine

LABEL maintainer "Threat Code"
LABEL description="IDSTools for downloading rules"

ARG GID=939
ARG UID=939
ARG USERNAME=socore
ARG VERSION=0.6.3

RUN apk add --no-cache --virtual .build-deps\
    shadow

RUN apk add --no-cache bash

RUN mkdir -p /opt/tc/idstools/bin && mkdir /opt/tc/idstools/etc
COPY entrypoint.sh /opt/tc/idstools/bin
RUN chmod +x /opt/tc/idstools/bin/entrypoint.sh && chown -R ${UID}:${GID} /opt/tc/idstools

RUN groupadd --gid ${GID} ${USERNAME} && \
    useradd --uid ${UID} --gid ${GID} \
    --home-dir /opt/so --no-create-home ${USERNAME}

RUN pip install https://github.com/jasonish/py-idstools/archive/master.zip

RUN apk del .build-deps

USER ${USERNAME}
WORKDIR /opt/tc/idstools/bin
ENTRYPOINT ["./entrypoint.sh"]
