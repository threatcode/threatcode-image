# This Dockerfile was based on the official Logstash Docker image:
# https://github.com/elastic/logstash-docker


ARG FLAVOR
ARG VERSION

FROM docker.elastic.co/logstash/$FLAVOR:$VERSION

LABEL maintainer "Threat Code"

USER root

ENV PATH=/usr/share/logstash/bin:$PATH

# Provide a minimal configuration, so that simple invocations will provide
# a good experience.
ADD config/logstash.yml config/log4j2.properties /usr/share/logstash/config/
ADD pipeline/default.conf /usr/share/logstash/pipeline/logstash.conf
ADD files/dictionaries/ /lib/dictionaries/
ADD files/freq /usr/share/logstash/pipeline.freq/
ADD files/domainstats /usr/share/logstash/pipeline.dstats/

RUN    ln -s /usr/share/logstash /opt/logstash \
    && mkdir /usr/share/logstash/pipeline.so \
    && mkdir /usr/share/logstash/pipeline.enabled \
    && chown --recursive 931:931 /usr/share/logstash \
    && chown --recursive 931:931 /lib/dictionaries

RUN groupmod -g 931 logstash && \
    usermod -u 931 -g 931 logstash && \
    groupadd -g 945 ossec && \
    usermod -a -G ossec logstash

# Ensure Logstash gets a UTF-8 locale by default.
ENV LANG='en_US.UTF-8' LC_ALL='en_US.UTF-8'

# Place the startup wrapper script.
ADD bin/docker-entrypoint /usr/local/bin/
RUN chmod 0755 /usr/local/bin/docker-entrypoint 

USER logstash

RUN cd /usr/share/logstash && LOGSTASH_PACK_URL=https://artifacts.elastic.co/downloads/logstash-plugins && \
  logstash-plugin install logstash-filter-translate \
                          logstash-filter-tld \
                          logstash-filter-elasticsearch \
                          logstash-filter-rest \
                          logstash-integration-kafka \
                          logstash-output-syslog

ENTRYPOINT ["/usr/local/bin/docker-entrypoint"]
