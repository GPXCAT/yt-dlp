"""Compare the official release with Docker Registry manifests."""
import base64
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

ACCEPT = ', '.join([
    'application/vnd.oci.image.index.v1+json',
    'application/vnd.docker.distribution.manifest.list.v2+json',
    'application/vnd.oci.image.manifest.v1+json',
    'application/vnd.docker.distribution.manifest.v2+json',
])


def fetch(url, headers=None):
    request = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def manifest_digest(image, tag, token):
    request = urllib.request.Request(
        f'https://registry-1.docker.io/v2/{image}/manifests/{tag}',
        headers={'Authorization': f'Bearer {token}', 'Accept': ACCEPT}, method='HEAD')
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            digest = response.headers['Docker-Content-Digest']
            if not digest:
                raise RuntimeError('Registry omitted content digest')
            return digest
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def decide(version_digest, latest_digest, force=False):
    build = force or version_digest is None
    publish = build or version_digest != latest_digest
    return build, publish


def main():
    image = os.environ['IMAGE']
    if not re.fullmatch(r'[a-z0-9_-]+/[a-z0-9_-]+', image):
        raise ValueError('Expected namespace/repository')
    user, password = os.environ['DOCKERHUB_USERNAME'], os.environ['DOCKERHUB_TOKEN']
    if not user or not password:
        raise ValueError('Configure Docker Hub username and token secrets')
    release = fetch('https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest', {
        'User-Agent': 'yt-dlp-autobuild', 'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + os.environ['GH_TOKEN']})
    version = release['tag_name']
    # yt-dlp tags look like 2025.11.12, with an optional hotfix suffix (.1).
    if release.get('prerelease') or release.get('draft') or not re.fullmatch(r'\d{4}\.\d{2}\.\d{2}(\.\d+)?', version):
        raise ValueError('Expected official YYYY.MM.DD release tag')
    auth = base64.b64encode(f'{user}:{password}'.encode()).decode()
    query = urllib.parse.urlencode({'service': 'registry.docker.io', 'scope': f'repository:{image}:pull'})
    token = fetch('https://auth.docker.io/token?' + query, {'Authorization': 'Basic ' + auth})['token']
    build, publish = decide(manifest_digest(image, version, token),
                            manifest_digest(image, 'latest', token),
                            os.getenv('FORCE', '').lower() == 'true')
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write(f'version={version}\nbuild={str(build).lower()}\npublish={str(publish).lower()}\n')
    print(f'Official version: {version}; build={build}; publish={publish}')


if __name__ == '__main__':
    main()
