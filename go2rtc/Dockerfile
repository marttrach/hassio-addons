# syntax=docker/dockerfile:1.7
ARG GO2RTC_REF=b5948cfb25404cc5cb37b166ecaa2dca20b11d4b
ARG GO_VERSION=1.25
ARG BUILD_FROM=ghcr.io/home-assistant/base-python:3.13-alpine3.22

FROM --platform=$BUILDPLATFORM golang:${GO_VERSION}-alpine AS build
ARG TARGETOS
ARG TARGETARCH
ARG GO2RTC_REF

RUN apk add --no-cache git python3
WORKDIR /src

RUN git clone https://github.com/AlexxIT/go2rtc.git . \
    && git checkout "${GO2RTC_REF}"

COPY scripts/apply-security-patches.py /tmp/apply-security-patches.py
RUN python3 /tmp/apply-security-patches.py

ENV GOOS=${TARGETOS}
ENV GOARCH=${TARGETARCH}
RUN CGO_ENABLED=0 go build -trimpath -ldflags "-s -w" -o /out/go2rtc .

FROM ${BUILD_FROM}
RUN apk add --no-cache tini ffmpeg ffplay bash curl jq alsa-plugins-pulse font-droid

ARG TARGETARCH
RUN if [ "${TARGETARCH}" = "amd64" ]; then apk add --no-cache libva-intel-driver intel-media-driver; fi

COPY --from=build /out/go2rtc /usr/local/bin/go2rtc

EXPOSE 1984 8554 8555 8555/udp
ENTRYPOINT ["/sbin/tini", "--"]
VOLUME ["/config"]
WORKDIR /config
CMD ["go2rtc", "-config", "/config/go2rtc.yaml"]
