from __future__ import unicode_literals
import requests
import click
import sys
import re
from itertools import groupby
from operator import itemgetter

QUALITY = {
    '1080p': ('8500_256', '.ts'),
    '720p': ('3500_256', '.ts'),
    'ac3': ('448', '.ac3')
}

proxies = {}


def get_artist_id(artist):
    params = dict(term=artist, entity='musicArtist', attribute='artistTerm', limit=1)
    resp = requests.get('https://itunes.apple.com/search', params=params, proxies=proxies)

    try:
        id = resp.json()['results'][0]['artistId']
    except IndexError:
        click.secho('Artist not found', fg='red')
        sys.exit(0)

    id_artist = '{}_{}'.format(id, artist)
    return id_artist


def generate_chapters(m3u8):
    songs = re.findall('#EXTINF:(.*),\r\n.*song(\d+).*\r\n', m3u8, re.MULTILINE)
    songtimes = [0]
    for song, segments in groupby(songs, itemgetter(1)):
        segment_len = sum(map(float, list(zip(*segments))[0]))
        songtimes.append(songtimes[-1] + segment_len)

    chapters = []
    chapter_t = 'CHAPTER{0:02d}={1}\nCHAPTER{0:02d}NAME=Song {0}'
    for n, chapter in enumerate(songtimes, 1):
        h, m = divmod(chapter, 3600)
        m, s = divmod(m, 60)
        chaps = ('{:02d}:{:02d}:{:06.3f}'.format(int(h), int(m), s))
        chapters.append(chapter_t.format(n, chaps))

    return '\n'.join(chapters)


@click.command()
@click.argument('day', type=click.IntRange(19, 28))
@click.argument('artist')
@click.argument('quality', default='1080p', type=click.Choice(['1080p', '720p', 'ac3']))
@click.option('--dump', '-d', is_flag=True, help='dump instead of downloading')
@click.option('--proxy', '-p', help='use http proxy')
@click.option('--chapters', '-c', is_flag=True, help='generate chapters')
def main(day, artist, quality, dump, proxy, chapters):
    '''
    Apple Music Festival 2015 Downloader
    '''

    stream, ext = QUALITY[quality]

    if proxy:
        proxies['http'] = proxy

    if '_' not in artist:
        artist = get_artist_id(artist)

    token = requests.get('https://itunes.apple.com/apps1b/authtoken/token.txt', proxies=proxies).text.strip()
    cookies = {'token': token}

    if dump:
        with open('token.txt', 'wt') as f:
            f.write('token={}'.format(token))

    output = '{}_{}_{}{}'.format(day, artist, quality, ext)

    files_url = 'http://streaming.itunesfestival.com/auth/eu1/vod/201509{}/v1/{}/{}_vod.m3u8'
    m3u8 = requests.get(files_url.format(day, stream, artist), cookies=cookies, allow_redirects=False, proxies=proxies)

    if 'performance_not_available' in m3u8.headers.get('location', ''):
        click.secho('Not available in your country, use proxy.', fg='red')
        return

    files = [i for i in m3u8.text.splitlines() if 'song' in i]

    total = len(files)
    if total == 0:
        click.secho('Recoding not available', fg='red')
        return

    if chapters:
        chapters_name = output.replace(ext, '_chapters.txt')
        with open(chapters_name, 'wt') as f:
            f.write(generate_chapters(m3u8.text))
        click.secho('Saved chapters to {}'.format(chapters_name), fg='green')

    if dump:
        m3u8_name = '{}'.format(output.replace(ext, '.m3u8'))
        with open(m3u8_name, 'wt') as f:
            f.write(m3u8.text)
        click.secho('Saved HLS playlist to {}'.format(m3u8_name), fg='green')
        return

    click.echo('Downloading {} parts to {}'.format(total, output))

    open(output, 'w').close()

    with click.progressbar(files, show_pos=True) as bar:
        for c, part in enumerate(bar, 1):
            part_url = 'http://streaming.itunesfestival.com/auth/eu1/vod/201509{}/v1/{}/{}'
            data = requests.get(part_url.format(day, stream, part), cookies=cookies, proxies=proxies)
            with open(output, 'ab') as f:
                f.write(data.content)

    click.secho('Done! Enjoy the show.', fg='green')


if __name__ == '__main__':
    main()
