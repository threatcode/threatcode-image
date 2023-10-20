FROM ghcr.io/threatcode/ubuntu:20.04

LABEL maintainer "Threat Code"
LABEL description="apt-cacher running in Docker container for use with Threat Code"

ARG GID=939
ARG UID=939
ARG USERNAME=socore

ENV APT_CACHER_NG_VERSION=3.6 \
    APT_CACHER_NG_CACHE_DIR=/var/cache/apt-cacher-ng \
    APT_CACHER_NG_LOG_DIR=/var/log/apt-cacher-ng \
    APT_CACHER_NG_USER=socore

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
      apt-cacher-ng ca-certificates\
 && rm -rf /var/lib/apt/lists/*

 # Create socore user.
RUN groupadd --gid ${GID} ${USERNAME} && \
    useradd --uid ${UID} --gid ${GID} \
    --home-dir /opt/so --no-create-home ${USERNAME}

COPY files/tc-entrypoint.sh /sbin/tc-entrypoint.sh
COPY repos/* /etc/apt-cacher-ng/

RUN chmod 755 /sbin/tc-entrypoint.sh && chown -R 939:939 /etc/apt-cacher-ng
RUN ln -sf /dev/stdout /var/log/apt-cacher-ng/apt-cacher.log; \
    ln -sf /dev/stderr /var/log/apt-cacher-ng/apt-cacher.err;

EXPOSE 3142/tcp

ENTRYPOINT ["/sbin/tc-entrypoint.sh"]

CMD ["/usr/sbin/apt-cacher-ng"]
