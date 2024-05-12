ARG ALPINE_TAG=latest
FROM alpine:${ALPINE_TAG}

RUN apk -U upgrade \
    && apk add --no-cache \
        nmap \
        nmap-scripts \
    && rm -rf /var/cache/apk/*