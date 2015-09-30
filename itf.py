from __future__ import unicode_literals
import requests
import click
import sys
import re
import os
from itertools import groupby
from operator import itemgetter
from concurrent.futures import ThreadPoolExecutor

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


def save_dump(token, basename, m3u8, urls):
    with open('token.txt', 'wt') as f:
            f.write('token={}'.format(token))

    m3u8_name = '{}.m3u8'.format(basename)
    with open(m3u8_name, 'wt') as f:
        f.write(m3u8)
    click.secho('Saved HLS playlist to {}'.format(m3u8_name), fg='green')

    urls_name = '{}.urls'.format(basename)
    with open(urls_name, 'wt') as f:
        f.write('\n'.join(urls))
    click.secho('Saved URLs to {}'.format(urls_name), fg='green')
    return


def download_part(args):
    url, cookies, proxies = args
    name = url.split('/')[-1]
    data = requests.get(url, cookies=cookies, proxies=proxies)
    with open(name, 'wb') as f:
        f.write(data.content)
    return name


@click.command()
@click.argument('day', type=click.IntRange(19, 28))
@click.argument('artist')
@click.argument('quality', default='1080p', type=click.Choice(['1080p', '720p', 'ac3']))
@click.option('--dump', '-d', is_flag=True, help='dump instead of downloading')
@click.option('--proxy', '-p', help='use http proxy')
@click.option('--chapters', '-c', is_flag=True, help='generate chapters')
@click.option('--threads', '-j', default=20, type=click.IntRange(1, 1000))
def main(day, artist, quality, dump, proxy, chapters, threads):
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

    output = '{}_{}_{}{}'.format(day, artist, quality, ext)

    files_url = 'http://streaming.itunesfestival.com/auth/eu1/vod/201509{}/v1/{}/{}_vod.m3u8'
    m3u8 = requests.get(files_url.format(day, stream, artist), cookies=cookies, allow_redirects=False, proxies=proxies)

    if 'performance_not_available' in m3u8.headers.get('location', ''):
        click.secho('Not available in your country, use proxy.', fg='red')
        return

    files = [i for i in m3u8.text.splitlines() if 'song' in i]

    part_url = 'http://streaming.itunesfestival.com/auth/eu1/vod/201509{}/v1/{}/{}'
    part_urls = [part_url.format(day, stream, part) for part in files]

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
        save_dump(token, output.replace(ext, ''), m3u8.text, part_urls)
        return

    click.echo('Downloading {} parts to {}'.format(total, output))

    open(output, 'w').close()

    pool = ThreadPoolExecutor(threads)
    parts = [(url, cookies, proxies) for url in part_urls]
    tasks = pool.map(download_part, parts)
    with click.progressbar(tasks, length=len(parts), show_pos=True) as bar:
        for name in bar:
            with open(name, 'rb') as f:
                data = f.read()
            with open(output, 'ab') as f:
                f.write(data)
            os.unlink(name)

    click.secho('Done! Enjoy the show.', fg='green')
    click.secho('\nHave an idea? https://github.com/banteg/itf')


if __name__ == '__main__':
    main()
