FROM python:3-alpine

RUN set -xe \
    && apk add --no-cache \
        ffmpeg \
    && pip3 install --no-cache-dir yt-dlp \
    && yt-dlp --version

ENTRYPOINT ["yt-dlp"]