

FROM ghcr.io/threatcode/python:3-slim

LABEL maintainer="Threat Code"
LABEL description="API for automating SOC-related functions"

WORKDIR /SOCtopus

RUN apt-get update && apt-get install -y --no-install-recommends git libmagic1 gcc python3-dev && rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/SigmaHQ/sigma.git && \
    mkdir -p /SOCtopus/templates && \
    mkdir -p /SOCtopus/playbook && \
    mkdir -p /var/log/SOCtopus

COPY ./tc-soctopus/requirements.txt /SOCtopus/

RUN pip install -r requirements.txt && \
    pip install gunicorn && \
    pip install bcrypt

COPY ./tc-soctopus /SOCtopus

# Temp Patch for 2.3.30 - fixes Sigmac Playbook issues
COPY ./elasticsearch.py /usr/local/lib/python3.9/site-packages/sigma/backends/elasticsearch.py

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:7000", "wsgi:app", "--log-file", "/var/log/SOCtopus/soctopus.log"]