# syntax=docker/dockerfile:1
FROM python:3-slim

RUN set -xe \
    && apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg curl unzip ca-certificates \
    && curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh \
    && apt-get purge -y curl unzip && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && deno --version

# Declared after the apt layer so a new version only rebuilds the pip layer.
ARG YTDLP_VERSION=latest
LABEL org.opencontainers.image.version="${YTDLP_VERSION}"
RUN set -xe \
    && if [ "$YTDLP_VERSION" = latest ]; then spec="yt-dlp[default]"; \
       else spec="yt-dlp[default]==$YTDLP_VERSION"; fi \
    && pip install --no-cache-dir "$spec" \
    && yt-dlp --version

WORKDIR /downloads
ENTRYPOINT ["yt-dlp"]
