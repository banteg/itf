## Apple Music Festival 2015 – Show Downloader

### Installation
Install [Python 3](https://www.python.org/downloads/), launch terminal and type:
```
pip install -U itf
```

### Usage
`itf --help` display help

`itf <day> <artist> [quality]` download specific show

### Options
`quality` 1080p, 720p or ac3 (default: 1080p)

`-p or --proxy` use http proxy, useful if performances are not available in your country

`-d or --dump` dump token and parts instead of downloading, useful if you don't like sequential downloads

### Examples
To download AC3 audio stream for Ellie Goulding, type
```
itf 19 elliegoulding ac3
```

To download 1080p performance of Take That via Tor, type:
```
itf 20 takethat -p 127.0.0.1:9050
```

To dump the urls for later use, type:
```
itf 19 andraday 720p --dump
```
Then you can download and merge the parts somewhat like that:
```
aria2c -c -j 10 --header="Cookie: {token.txt}" -i parts.txt
cat *.ts > andraday.ts
```

### Note on ac3 muxing
Audio in ac3 stream can be slightly out of sync with ts. The best method is to extract first minute or so, find the delay (you can do it automatically and prescisely [with my other project](https://github.com/banteg/audos)), then fix the ac3 with [delaycut](http://www.videohelp.com/software/delaycut) and then mux with ffmpeg.

```
ffmpeg -i v.ts -t 60 v.wav
ffmpeg -i a.ac3 -t 60 a.wav
audos v.wav a.wav
delaycut
ffmpeg -i v.ts -i a_cut.ac3 -map 0:0 -map 0:1 -map 1 -absf aac_adtstoasc -c copy out.mp4
```
