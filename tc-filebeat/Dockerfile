# This Dockerfile was based on the official Filebeat Docker image:
# https://hub.docker.com/r/elastic/filebeat/


ARG FLAVOR
ARG VERSION

FROM docker.elastic.co/beats/$FLAVOR:$VERSION
USER root
# Add entrypoint wrapper script
ADD files/docker-entrypoint /usr/local/bin
RUN chmod 755 /usr/local/bin/docker-entrypoint

# Provide a non-root user.
RUN groupadd --gid 939 socore && \
    useradd -M --uid 939 --gid 939 --home /usr/share/filebeat socore && \
    groupadd -g 945 ossec && \
    usermod -a -G ossec socore

WORKDIR /usr/share/filebeat
RUN chown -R root:socore . && \
    find /usr/share/filebeat -type d -exec chmod 0750 {} \; && \
    find /usr/share/filebeat -type f -exec chmod 0640 {} \; && \
    chmod 0750 filebeat && \
    chmod 0770 modules.d && \
    chmod 0770 data logs
USER socore
ENTRYPOINT ["/usr/local/bin/docker-entrypoint"]
CMD ["-c", "/usr/share/filebeat/filebeat.yml"]
