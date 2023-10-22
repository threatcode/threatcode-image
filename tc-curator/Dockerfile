FROM alpine:3

LABEL maintainer "Threat Code" 

ARG GID=934
ARG UID=934
ARG USERNAME=curator

ENV LC_ALL=en_US.UTF-8

USER root

RUN apk --no-cache add python3 py-setuptools py-pip gcc libffi py-cffi python3-dev libffi-dev py-openssl musl-dev linux-headers openssl-dev && \
    pip install elasticsearch-curator && \
    apk del gcc python3-dev libffi-dev musl-dev linux-headers openssl-dev

RUN addgroup -g ${GID} ${USERNAME} && \
    adduser -u ${UID} -G ${USERNAME} -D -H ${USERNAME}

COPY ../files/actions.py /usr/lib/python3.10/site-packages/curator/actions.py
COPY ../files/settings.py /usr/lib/python3.10/site-packages/curator/defaults/settings.py 
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER curator

ENTRYPOINT [ "/entrypoint.sh" ]
