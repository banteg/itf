from __future__ import unicode_literals, print_function
import requests
import click

QUALITY = {
    '1080p': ('8500_256', '.ts'),
    '720p': ('3500_256', '.ts'),
    'ac3': ('448', '.ac3')
}


def get_artist_id(artist):
    params = dict(term=artist, entity='musicArtist', attribute='artistTerm', limit=1)
    resp = requests.get('https://itunes.apple.com/search', params=params)
    id = resp.json()['results'][0]['artistId']
    id_artist = '{}_{}'.format(id, artist)
    return id_artist


@click.command()
@click.argument('day', type=click.IntRange(19, 28))
@click.argument('artist')
@click.argument('quality', default='1080p', type=click.Choice(['1080p', '720p', 'ac3']))
@click.option('--dump', '-d', is_flag=True, help='dump token and urls instead of downloading')
@click.option('--proxy', '-p', help='specify proxy')
def main(day, artist, quality, dump, proxy):
    '''
    Apple Music Festival 2015 Downloader
    '''

    stream, ext = QUALITY[quality]

    if '_' not in artist:
        artist = get_artist_id(artist)

    token = requests.get('https://itunes.apple.com/apps1b/authtoken/token.txt').text
    cookies = {'token': token}

    output = '{}_{}_{}{}'.format(day, artist, quality, ext)

    files_url = 'http://streaming.itunesfestival.com/auth/eu1/vod/201509{}/v1/{}/{}_vod.m3u8'
    files = requests.get(files_url.format(day, stream, artist), cookies=cookies, allow_redirects=False)

    if 'performance_not_available' in files.headers.get('location', ''):
        print('Not available in your country, use proxy.')
        return

    files = [i for i in files.text.splitlines() if 'song' in i]

    total = len(files)
    print('Downloading {} parts to {}'.format(total, output))

    open(output, 'w').close()

    for c, part in enumerate(files, 1):
        print('Downlading part {}/{} {}'.format(c, total, part))
        part_url = 'http://streaming.itunesfestival.com/auth/eu1/vod/201509{}/v1/{}/{}'
        data = requests.get(part_url.format(day, stream, part), cookies=cookies)
        with open(output, 'ab') as f:
            f.write(data.content)

    print('Done! Enjoy the show.')


if __name__ == '__main__':
    main()
