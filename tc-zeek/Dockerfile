FROM ghcr.io/threatcode/rockylinux:8 as builder 
RUN dnf -y install dnf-plugins-core && dnf config-manager --set-enabled powertools && dnf update -y && \
    dnf -y install epel-release bash libpcap iproute wget cmake swig && \
    dnf -y install jemalloc numactl libnl3 libdnet gdb GeoIP git && \
    dnf -y install libpcap-devel openssl-devel zlib-devel jemalloc-devel python3-devel kernel-devel kernel-headers &&\
    dnf group install -y "Development Tools" && \
    pip3 install GitPython semantic-version requests && \
    dnf -y erase epel-release && dnf clean all && rm -rf /var/cache/dnf

ENV ZEEKVER=5.0.10
ARG BUILD_TYPE=Release

RUN mkdir /zeekbuild

WORKDIR /zeekbuild

RUN wget https://download.zeek.org/zeek-$ZEEKVER.tar.gz && tar zxvf zeek-$ZEEKVER.tar.gz
RUN cd zeek-$ZEEKVER && \
    ./configure --prefix=/opt/zeek --spooldir=/nsm/zeek/spool --logdir=/nsm/zeek/logs --enable-jemalloc --build-type=$BUILD_TYPE && \
    make -j4 && make install 
RUN yum install -y glibc-common
RUN /opt/zeek/bin/zkg install --force ja3 && \
    /opt/zeek/bin/zkg install --force hassh && \
    /opt/zeek/bin/zkg install --force https://github.com/TOoSmOotH/zeek-af_packet-plugin --version=master && \
    /opt/zeek/bin/zkg install --force zeek-community-id && \
    #/opt/zeek/bin/zkg install --force bzar && \
    /opt/zeek/bin/zkg install --force --skiptests https://github.com/mmguero-dev/bzar --version=master && \
    /opt/zeek/bin/zkg install --force --skiptests icsnpp-bacnet && \
    /opt/zeek/bin/zkg install --force --skiptests icsnpp-bsap && \
    /opt/zeek/bin/zkg install --force --skiptests icsnpp-ethercat && \
    /opt/zeek/bin/zkg install --force --skiptests icsnpp-enip && \
    /opt/zeek/bin/zkg install --force --skiptests icsnpp-opcua-binary && \
    sed -i 's|-|_|g' /opt/zeek/share/zeek/site/icsnpp-opcua-binary/main.zeek && \
    /opt/zeek/bin/zkg install --force --skiptests icsnpp-dnp3 && \
    /opt/zeek/bin/zkg install --force --skiptests icsnpp-modbus && \
    git clone https://github.com/cisagov/icsnpp-s7comm && \
    /opt/zeek/bin/zkg install --force --skiptests icsnpp-s7comm && \
    git clone https://github.com/amzn/zeek-plugin-profinet && \
    /opt/zeek/bin/zkg install --force --skiptests zeek-plugin-profinet && \
    git clone https://github.com/amzn/zeek-plugin-tds && \
    /opt/zeek/bin/zkg install --force --skiptests zeek-plugin-tds && \
    /opt/zeek/bin/zkg install --force --skiptests zeek-spicy-wireguard && \ 
    /opt/zeek/bin/zkg install --force --skiptests zeek-spicy-stun && \
    /opt/zeek/bin/zkg install --force --skiptests https://github.com/iamckn/oui-logging && \
    /bin/python3 /opt/zeek/share/zeek/site/oui-logging/oui.py /opt/zeek/share/zeek/site/oui-logging/oui.dat && \
    rm -rf /opt/zeek/var/lib/zkg/testing && \
    rm -rf /opt/zeek/var/lib/zkg/scratch
RUN groupadd --gid 937 zeek  && \
    adduser --uid 937 --gid 937 --home-dir /opt/zeek --no-create-home zeek && \
    chown -R 937:937 /opt/zeek && \
    chown -R 937:937 /nsm/zeek
    
FROM ghcr.io/threatcode/rockylinux:8 

LABEL maintainer "Threat Code"
LABEL description="Zeek running in a docker with AF_Packet 3.2.0 for use with Threat Code."

# Common CentOS layer
RUN dnf update -y && \
    dnf -y install epel-release bash findutils libpcap iproute && \
    dnf -y install jemalloc numactl libnl3 libdnet gdb GeoIP python3 && \
    dnf -y erase epel-release && dnf clean all && rm -rf /var/cache/dnf && \
    groupadd --gid 937 zeek  && \
    adduser --uid 937 --gid 937 --home-dir /opt/zeek --no-create-home zeek
    
COPY --from=builder /nsm/zeek /nsm/zeek
COPY --from=builder /opt/zeek /opt/zeek

# Copy over the entry script.
COPY files/zeek.sh /usr/local/sbin/zeek.sh
RUN chmod +x /usr/local/sbin/zeek.sh
RUN rpm -i https://github.com/axellioinc/fx-libpcap/releases/download/fxlibpcap-1.9.1/fx-libpcap-1.9.1-1.el7.x86_64.rpm

HEALTHCHECK --interval=10m --timeout=2m CMD /opt/zeek/bin/zeekctl status || (kill -s 15 -1 && (sleep 30; kill -s 9 -1))

ENTRYPOINT ["/usr/local/sbin/zeek.sh"]
