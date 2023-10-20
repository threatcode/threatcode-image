FROM ghcr.io/threatcode/redis:6-alpine
LABEL maintainer "Threat Code"
LABEL description="REDIS running in Docker container for use with Threat Code"
RUN addgroup -g 939 socore && adduser -D --uid 939 --ingroup socore socore && \
    chown 939:939 /data
VOLUME /data
WORKDIR /data
EXPOSE 6379
CMD ["redis-server"]
