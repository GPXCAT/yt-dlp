FROM python:3-slim

RUN set -xe \
    && apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg curl unzip ca-certificates \
    && curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh \
    && apt-get purge -y curl unzip && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir "yt-dlp[default]" \
    && yt-dlp --version \
    && deno --version

WORKDIR /downloads
ENTRYPOINT ["yt-dlp"]
