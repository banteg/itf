import requests
import sys
import re

print('iTunes Festival London 2014 Downloader\n')

QUALITY = {
    '1080p': ('8500_256', '.ts'),
    '720p': ('3500_256', '.ts'),
    'ac3': ('448', '.ac3')
}


def usage():
    print('''Usage:
    python itf.py
    python itf.py shows
    python itf.py <day> <artist> [quality]

Options:
    quality  1080p, 720p or ac3 (default: 1080p)''')


def shows_available():
    print('Shows available to download:\n')

    atv = requests.get('https://appletv.itunesfestival.com/1b/en-GB/gb.json').json()['video_dict']
    vods = [atv[x] for x in atv if x.startswith('vod')]
    shows = []

    for show in vods:
        tag, artist = re.search('201409(\d{2})/v\d/(.*)_atv_vod\.m3u8', show['url']).groups()
        shows.append((show['title'], tag, artist))

    shows = sorted(shows, key=lambda x: x[1])
    for show in shows:
        print('{}\npython itf.py {} {}\n'.format(*show))


def download_show(tag, artist, quality='1080p'):
    stream, ext = QUALITY[quality]
    token = requests.get('http://itunes.apple.com/apps1b/authtoken/token.txt').text
    cookies = {'token': token}
    output = artist.split('_')[-1] + ext

    files_url = 'http://streaming.itunesfestival.com/auth/eu1/vod/201409{}/v1/{}/{}_vod.m3u8'.format(tag, stream, artist)
    files = requests.get(files_url, cookies=cookies)

    files = [i for i in files.text.splitlines() if not i.startswith('#')]

    total = len(files)
    print('Downloading {} parts to {}'.format(total, output))
    open(output, 'w').close()

    for c, part in enumerate(files, start=1):
        print('Downlading part {}/{} {}'.format(c, total, part))
        part_url = 'http://streaming.itunesfestival.com/auth/eu1/vod/201409{}/v1/{}/{}'.format(tag, stream, part)
        data = requests.get(part_url, cookies=cookies)
        with open(output, 'ab') as f:
            f.write(data.content)

    print('Done! Enjoy the show.')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        shows_available()
    elif len(sys.argv) == 3:
        _, tag, artist = sys.argv
        download_show(tag, artist)
    elif len(sys.argv) == 4:
        _, tag, artist, quality = sys.argv
        if not quality in QUALITY:
            print('Warning: unknown quality, defaulting to 1080p')
            quality = '1080p'
        download_show(tag, artist, quality=quality)
    else:
        usage()
