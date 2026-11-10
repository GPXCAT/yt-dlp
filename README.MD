# yt-dlp Docker 自動建置

GitHub Actions 每小時檢查 yt-dlp 官方最新正式版（https://github.com/yt-dlp/yt-dlp/releases）。若 Docker Hub 還沒有對應版本，便自動建置並推送 `jscat/yt-dlp:YYYY.MM.DD`，成功後再更新 `jscat/yt-dlp:latest`，最後通知 Discord。無新版本則不建置、不通知。

## 設定

1. 在 Docker Hub 建立或確認 `jscat/yt-dlp` repository。
2. GitHub repository → Settings → Secrets and variables → Actions → New repository secret，新增：

| Secret | 值 |
| --- | --- |
| DOCKERHUB_USERNAME | jscat |
| DOCKERHUB_TOKEN | Docker Hub 建立的 access token，需有此 repository 的 Read & Write 權限 |
| DISCORD_WEBHOOK_URL | Discord 頻道的 incoming webhook 完整網址；可省略而不通知 |

不要把 access token 或 webhook 寫入程式、Dockerfile 或 Git。

3. 把檔案提交到預設分支（main），開啟 GitHub Actions。
4. Actions → Publish yt-dlp image → Run workflow，首次先手動執行。

排程每小時第 27 分執行（UTC）。GitHub 排程可能延遲；公開 repository 若 60 天沒有活動，排程可能被自動停用，需重新啟用。

## 注意事項

- yt-dlp 以 pip 從 PyPI 安裝指定版本。若 GitHub 已發佈 Release、但 PyPI 尚未上架，建置會失敗，下次排程會再試。
- 修改 Dockerfile 不會自動重建既有版本。手動 Run workflow 並勾選 force 可重建當前版本，會覆寫該版本標籤與 latest。
- 排程只處理當時最新正式版，不補建中間版本。

## Build：本機

```bash
# 不指定版本時安裝 PyPI 上最新版
docker build -t jscat/yt-dlp .

# 指定版本
docker build --build-arg YTDLP_VERSION=2025.11.12 -t jscat/yt-dlp:2025.11.12 .
```

## Build：多平台並推送 Docker Hub

```bash
VERSION=2025.11.12
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --build-arg YTDLP_VERSION="$VERSION" \
  -t "jscat/yt-dlp:$VERSION" \
  -t jscat/yt-dlp:latest \
  --push .
```

## Run

```bash
docker run --rm -it \
    -v $(pwd):/downloads \
    jscat/yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
    --merge-output-format mp4 https://www.youtube.com/watch?v=iVAWwYzAlVs
```

## Install docker

https://docs.docker.com/engine/install/ubuntu/
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

yt-dlp documentation: https://github.com/yt-dlp/yt-dlp
