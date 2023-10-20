

FROM ghcr.io/threatcode/centos:7 as builder

RUN yum -y install epel-release
RUN yum -y install jansson-devel libpcap-devel python3 libpcap-devel openssl-devel zlib-devel jemalloc-devel python3-devel kernel-devel kernel-headers libjansson libgeoip liblua5.1 curl wget make gcc pkg-config libhiredis libevent pcre-devel libpcre libmagic zlib libyaml rustc cargo libyaml-devel libcap-ng-devel file-devel nss-devel nspr-devel python3-yaml luajit-devel luajit

ENV SURIVERSION=6.0.14
RUN mkdir /suricata

WORKDIR /suricata

RUN curl -vO https://www.openinfosecfoundation.org/download/suricata-$SURIVERSION.tar.gz && tar zxvf suricata-$SURIVERSION.tar.gz && \
    cd suricata-$SURIVERSION && ./configure --enable-rust --enable-luajit --prefix=/opt/suricata --sysconfdir=/etc --disable-gccmarch-native --localstatedir=/var && make
RUN mkdir suriinstall && cd suricata-$SURIVERSION && make install DESTDIR=/suricata/suriinstall && make install-conf DESTDIR=/suricata/suriinstall && rm -rf /suricata/suriinstall/var/run

FROM ghcr.io/threatcode/centos:7

LABEL maintainer "Threat Code"
LABEL description="Suricata running in a docker with AF_Packet for use with Threat Code."

COPY --from=builder /suricata/suriinstall/ /

RUN yum -y install epel-release bash libpcap iproute && \
    yum -y install GeoIP luajit libnet jansson libyaml cargo rustc && \
    yum -y erase epel-release && yum clean all && rm -rf /var/cache/yum && \
    groupadd --gid 940 suricata && \
    adduser --uid 940 --gid 940 --home-dir /etc/suricata --no-create-home suricata && \
    chown -R 940:940 /etc/suricata && \
    chown -R 940:940 /var/log/suricata

# Copy over the entry script.
ADD files/tc-suricata.sh /usr/local/sbin/tc-suricata.sh

RUN chmod +x /usr/local/sbin/tc-suricata.sh
RUN rpm -i https://github.com/axellioinc/fx-libpcap/releases/download/fxlibpcap-1.9.1/fx-libpcap-1.9.1-1.el7.x86_64.rpm

ENTRYPOINT ["/usr/local/sbin/tc-suricata.sh"]
