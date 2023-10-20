# This Dockerfile was based on the official Kibana Docker image:
# https://github.com/elastic/kibana-docker


ARG FLAVOR
ARG VERSION

FROM docker.elastic.co/kibana/$FLAVOR:$VERSION

USER root

# Files are owned by 1000:1000 by default.
# This causes Kibana to fail on startup.
# Set ownership to kibana:kibana.
RUN chown --recursive 932:932 /usr/share/kibana/*

RUN groupmod -g 932 kibana && usermod -u 932 -g 932 kibana

WORKDIR /usr/share/kibana
RUN  ln -s /usr/share/kibana /opt/kibana

ENV PATH=/usr/share/kibana/bin:$PATH

# Copy over the dashboards
RUN mkdir /usr/share/kibana/dashboards

# Add a self-signed SSL certificate for use in examples.
#ADD ssl/kibana.example.org.* /usr/share/kibana/config/

# Add the launcher/wrapper script. It knows how to interpret environment
# variables and translate them to Kibana CLI options.
ADD bin/kibana-docker /usr/local/bin/

# Add our custom Threat Code Entry Script
ADD bin/tc-kibana.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/tc-kibana.sh

## Switch to limited user and run process.
USER kibana
#CMD /usr/local/bin/kibana-docker

ENTRYPOINT ["/usr/local/bin/tc-kibana.sh"]
