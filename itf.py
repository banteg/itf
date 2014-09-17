import requests
import sys
import re

print('iTunes Festival London 2014 Downloader\n')


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


def download_show():
    _, tag, artist = sys.argv

    token = requests.get('http://itunes.apple.com/apps1b/authtoken/token.txt').text
    cookies = {'token': token}
    output = artist.split('_')[-1] + '.ts'

    files_url = 'http://streaming.itunesfestival.com/auth/eu1/vod/201409{}/v1/8500_256/{}_vod.m3u8'.format(tag, artist)
    files = requests.get(files_url, cookies=cookies)

    files = [i for i in files.text.splitlines() if not i.startswith('#')]

    total = len(files)
    print('Downloading {} parts to {}'.format(total, output))

    for c, part in enumerate(files, start=1):
        print('Downlading part {}/{} {}'.format(c, total, part))
        part_url = 'http://streaming.itunesfestival.com/auth/eu1/vod/201409{}/v1/8500_256/{}'.format(tag, part)
        data = requests.get(part_url, cookies=cookies)
        with open(output, 'ab') as f:
            f.write(data.content)

    print('Done! Enjoy the show.')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        shows_available()
    else:
        download_show()
