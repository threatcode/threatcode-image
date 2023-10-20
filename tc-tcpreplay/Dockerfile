

FROM ghcr.io/threatcode/centos:7

LABEL maintainer "Threat Code"
LABEL description="Replay PCAPs to sniffing interface(s)"

# Copy over tcpreplay - using v4.2.6 instead of 4.3.x because of known bugs: https://github.com/appneta/tcpreplay/issues/557
COPY files/tcpreplay /usr/local/bin/tcpreplay

# Setup our utilities, download the pcap samples, convert them to RPM and install them
RUN yum update -y && \
    yum clean all && \
    yum -y install epel-release && \
    yum -y install libpcap && \
    yum -y install rpmrebuild && \
    yum -y install alien && \
    yum -y install wget && \
\
for i in threatcode-samples_20121202-0ubuntu0threatcode4_all.deb threatcode-samples-bro_20170824-1ubuntu1threatcode3_all.deb threatcode-samples-markofu_20130522-0ubuntu0threatcode3_all.deb threatcode-samples-mta_20190514-1ubuntu1threatcode1_all.deb threatcode-samples-shellshock_20140926-0ubuntu0threatcode2_all.deb; do wget https://launchpad.net/~threatcode/+archive/ubuntu/stable/+files/$i; done && \
\ 
alien -r *.deb && \
\
for i in threatcode-samples-20121202-1.noarch.rpm threatcode-samples-bro-20170824-2.noarch.rpm threatcode-samples-markofu-20130522-1.noarch.rpm threatcode-samples-mta-20190514-2.noarch.rpm threatcode-samples-shellshock-20140926-1.noarch.rpm  ; do rpmrebuild -p --change-spec-files='sed -e "s/%dir.*\"\/\"/#/"' -d/tmp/ $i && rpm -ivh /tmp/noarch/$i; done && \
\
rm *.deb && \
rm *.rpm

ENTRYPOINT ["/bin/bash"]

