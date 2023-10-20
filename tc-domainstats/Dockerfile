

FROM ghcr.io/threatcode/python:3-alpine

LABEL maintainer "Threat Code"
LABEL description="Domainstats running in Docker container for use with Threat Code"

ARG GID=936
ARG UID=936
ARG USERNAME=domainstats

RUN apk add --no-cache --virtual .build-deps\
    shadow \
    git

RUN apk add --no-cache bash

RUN groupadd --gid ${GID} ${USERNAME} && \
    useradd --uid ${UID} --gid ${GID} --no-create-home ${USERNAME}

RUN cd /opt && \
	git clone -b domain_stats_1 https://github.com/MarkBaggett/domain_stats.git && \
	mkdir /var/log/domain_stats && \
	ln -sf /dev/stderr /var/log/domain_stats/domain_stats.log && \
	chown -R ${UID}:${GID} /opt/domain_stats

RUN pip install --no-cache-dir six python-whois
RUN apk del .build-deps

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 20000
STOPSIGNAL SIGTERM

USER ${USERNAME}

ENTRYPOINT [ "/entrypoint.sh" ]
