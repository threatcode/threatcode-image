FROM ghcr.io/threatcode/telegraf:1.20.3-alpine
LABEL maintainer "Threat Code"
LABEL description="Telegraf running in Docker container for use with Threat Code"

USER root

RUN apk add --no-cache redis curl jq

ENTRYPOINT ["/entrypoint.sh"]
CMD ["telegraf"]
