# This Dockerfile was based on the official Elasticsearch Docker image:
# https://github.com/elastic/elasticsearch-docker


ARG FLAVOR
ARG VERSION

FROM docker.elastic.co/elasticsearch/$FLAVOR:$VERSION

ARG GID=930
ARG UID=930
ARG USERNAME=elasticsearch
ARG FLAVOR

USER root 
RUN groupmod -g ${GID} ${USERNAME} && \
    usermod -u ${UID} -g ${GID} ${USERNAME}

WORKDIR /usr/share/elasticsearch

RUN set -ex && for esdirs in config data logs; do \
        mkdir -p "$esdirs"; \
        chown -R elasticsearch:elasticsearch "$esdirs"; \
    done

COPY *.yml log4j2.properties config/
COPY bin bin


RUN apt-get update && apt-get install -y ca-certificates unzip wget && \
    wget -O /tmp/GeoLite2.zip https://github.com/ThreatCode/threatcode-docker-rpm/releases/download/geolite2-db/GeoLite2.zip && \
    mkdir -p /usr/share/elasticsearch/config/ingest-geoip && \
    unzip -o /tmp/GeoLite2.zip -d /usr/share/elasticsearch/config/ingest-geoip && \
    apt-get remove -y unzip wget && \
    rm -rf /var/lib/apt/lists/*

RUN chown elasticsearch:elasticsearch config/elasticsearch.yml config/log4j2.properties bin/es-docker /usr/share/elasticsearch/config/ingest-geoip && \
    chmod 0750 bin/es-docker

# Enable the following lines if custom plugins are to be included in this image.
# COPY plugins-src /plugins-src
# RUN bin/build-plugins /plugins-src plugins/

USER ${USERNAME}
CMD ["/bin/bash", "bin/es-docker"]
