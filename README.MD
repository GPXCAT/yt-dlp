# build
```bash
docker build -t jscat/yt-dlp .
```

# build multi platform
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t jscat/yt-dlp:2024.04.09 -t jscat/yt-dlp:latest --push .
```

# run
```bash
docker run --rm -it \
    -v $(pwd):/app -w /app \
    jscat/yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
    --merge-output-format mp4 https://www.youtube.com/watch?v=iVAWwYzAlVs
```

# install docker
https://docs.docker.com/engine/install/ubuntu/
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

yt-dlp documentation: https://github.com/yt-dlp/yt-dlp