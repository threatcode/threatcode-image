

FROM ghcr.io/threatcode/alpine
LABEL maintainer "Threat Code"
LABEL description="Fleet running in Docker container for use with Threat Code"

RUN apk --update add ca-certificates unzip curl bash

COPY startfleet.sh /startfleet.sh
RUN chmod +x /startfleet.sh

RUN mkdir -p /tmp/fleet && cd /tmp/fleet \
&& curl -OL  https://github.com/fleetdm/fleet/releases/download/fleet-v4.31.1/fleet_v4.31.1_linux.tar.gz \
&& curl -OL https://github.com/fleetdm/fleet/releases/download/fleet-v4.31.1/fleetctl_v4.31.1_linux.tar.gz \
&& for file in *.tar.gz; do tar -zxf "$file"; done \
&& cp fleet_*_linux/fleet /usr/bin/fleet \
&& cp fleetctl_*_linux/fleetctl /usr/bin/fleetctl \
&& cd /tmp && rm -rf /tmp/fleet

ENTRYPOINT ["/startfleet.sh"]
