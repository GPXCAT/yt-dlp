import json
import os
import urllib.parse
import urllib.request


def main():
    webhook = os.getenv('DISCORD_WEBHOOK_URL', '')
    if not webhook:
        print('Discord notification skipped: webhook secret is not configured')
        return
    ok = os.getenv('RESULT') == 'success'
    image = os.environ['IMAGE']
    version = os.getenv('VERSION') or '(check failed)'
    content = (f'✅ Docker image 發佈完成：{image}:{version}\n同步更新 {image}:latest'
               if ok else f'❌ yt-dlp 自動建置／發佈失敗：{version}')
    content += '\n' + os.environ['RUN_URL']
    parts = urllib.parse.urlsplit(webhook)
    query = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query) if k != 'wait']
    query.append(('wait', 'true'))
    url = urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(query)))
    payload = json.dumps({'content': content, 'allowed_mentions': {'parse': []}}, ensure_ascii=False).encode()
    request = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json', 'User-Agent': 'yt-dlp-autobuild'})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            message = json.load(response)
            if not message.get('id'):
                raise RuntimeError('Message creation not confirmed')
    except Exception:
        # Do not expose the webhook URL/token in a traceback.
        raise SystemExit('Discord notification failed; inspect the workflow result and webhook configuration') from None


if __name__ == '__main__':
    main()
