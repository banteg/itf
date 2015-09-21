from __future__ import unicode_literals
import requests
import click
import sys

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


@click.command()
@click.argument('day', type=click.IntRange(19, 28))
@click.argument('artist')
@click.argument('quality', default='1080p', type=click.Choice(['1080p', '720p', 'ac3']))
@click.option('--dump', '-d', is_flag=True, help='dump instead of downloading')
@click.option('--proxy', '-p', help='use http proxy')
def main(day, artist, quality, dump, proxy):
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
    files = requests.get(files_url.format(day, stream, artist), cookies=cookies, allow_redirects=False, proxies=proxies)

    if 'performance_not_available' in files.headers.get('location', ''):
        click.secho('Not available in your country, use proxy.', fg='red')
        return

    files = [i for i in files.text.splitlines() if 'song' in i]

    total = len(files)
    if total == 0:
        click.secho('Recoding not available', fg='red')
        return

    if dump:
        with open('{}.txt'.format(output), 'wt') as f:
            f.write('\n'.join(files))
        click.secho('Dumped {} parts to {}.txt'.format(total, output), fg='green')
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
