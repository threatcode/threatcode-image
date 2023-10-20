

FROM ghcr.io/threatcode/centos:7

LABEL maintainer "Threat Code"
LABEL description="Google Stenographer running in a docker for use with Threat Code."

# Common CentOS layer
RUN yum -y install epel-release bash libpcap iproute && \
    yum -y install https://repo.ius.io/ius-release-el7.rpm && \
    yum -y install snappy leveldb tcpdump jq libaio libseccomp golang which openssl python36u python36u-pip && \
    /usr/bin/pip3.6 install && \
    yum -y erase epel-release && yum clean all && rm -rf /var/cache/yum && \
    rpm -i https://github.com/ThreatCode/threatcode-docker-rpm/releases/download/Stenoupgrade/stenographer-0-1.20200922gite8db1ee.el7.x86_64.rpm && \
    setcap 'CAP_NET_RAW+ep CAP_NET_ADMIN+ep CAP_IPC_LOCK+ep CAP_SETGID+ep' /usr/bin/stenotype && \
    mkdir -p /nsm/pcap/files && \
    mkdir -p /nsm/pcap/index && \
    chown -R 941:941 /nsm/pcap && \
    mkdir -p /etc/stenographer/certs && \
    mkdir -p /var/log/stenographer && \
    usermod -s /bin/bash stenographer


# Copy over the entry script.
COPY files/tc-steno.sh /usr/local/sbin/tc-steno.sh
RUN chmod +x /usr/local/sbin/tc-steno.sh

ENTRYPOINT ["/usr/local/sbin/tc-steno.sh"]
