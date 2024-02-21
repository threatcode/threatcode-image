

# Navigator build stage
FROM ghcr.io/threatcode/node:16-alpine as navigator-builder

ARG NAVIGATOR_VERSION=4.6.4

RUN apk add git && \
    git config --global advice.detachedHead false && \
    git clone -b "v${NAVIGATOR_VERSION}" https://github.com/mitre-attack/attack-navigator.git

WORKDIR /attack-navigator/nav-app/

RUN npm ci && npx ng build

# Delete base href line from index html to fix url path issues
RUN sed -i '/<base href="\/">/d' ./dist/index.html

###################################

FROM nginx:1.25.1-alpine

LABEL maintainer "Threat Code"
LABEL description="Threat Code Core Functions Docker"

ARG CYBERCHEF_VERSION=10.5.2

RUN mkdir -p /opt/socore/html/navigator
COPY --from=navigator-builder /attack-navigator/nav-app/dist /opt/socore/html/navigator

RUN mkdir -p /opt/socore/html/cyberchef && \
    wget -O /tmp/CyberChef.zip https://github.com/gchq/CyberChef/releases/download/v${CYBERCHEF_VERSION}/CyberChef_v${CYBERCHEF_VERSION}.zip  && \
    unzip -o /tmp/CyberChef.zip -d /opt/socore/html/cyberchef && \
    mv /opt/socore/html/cyberchef/CyberChef_v${CYBERCHEF_VERSION}.html /opt/socore/html/cyberchef/index.html && \
    rm -f /tmp/CyberChef.zip

EXPOSE 80
EXPOSE 443
