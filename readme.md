## Apple Music Festival 2015 – Show Downloader

### Installation
Install [Python 3](https://www.python.org/downloads/), launch terminal and type:
```
pip install -U itf
```
On Linux type:
```
sudo pip3 install -U itf
```

### Usage
`itf --help` display help

`itf <day> <artist> [quality]` download specific show

### Options
`quality` 1080p, 720p or ac3 (default: 1080p)

`-p or --proxy` use http proxy, useful if performances are unavailable in your country

`-d or --dump` dump token and parts instead of downloading, useful if you don't like sequential downloads

`-c or --chapters` save chapters file, note that you'll need to add song names manually and then mux it (see below).

`-j or --threads` downloading using multiple threads (1–1000, default: 20)

### Examples
To download AC3 audio stream for Ellie Goulding, type
```
itf 19 elliegoulding ac3
```

To download 1080p performance of Take That via Tor, type:
```
itf 20 takethat -p 127.0.0.1:9050
```

To dump hls playlist, urls and chapters for later use, type:
```
itf 19 andraday 720p --dump --chapters
```
Then you can download and merge parts:
```
aria2c -c -j 10 -d parts --header="Cookie: {contents of token.txt}" -i parts.txt
cat parts/*.ts > video.ts
```
Also you can edit song names in chapter file and mux everything with with [Yamb](http://www.videohelp.com/software/YAMB) (on Windows) or [Subler](http://videohelp.com/software/Subler) (on Mac).

### Notes
It might be a good idea to remux `.ts` file to `.mp4`, use Yamb or Subler, don't use ffmpeg.

Audio in `.ac3` stream might be slightly out of sync. Delay/rush can be fixed with [delaycut](http://www.videohelp.com/software/delaycut).
