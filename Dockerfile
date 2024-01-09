FROM python:3.10.11-slim-bullseye

RUN python3 -m pip --no-cache-dir install yt-dlp

RUN apt-get update \
    && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/list/*

ENTRYPOINT ["yt-dlp"]