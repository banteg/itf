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

`-c or --chapters` save chapters file, note that you'll need to add song names manually and then mux it all with mkvmerge

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
aria2c -c -j 10 --header="Cookie: {token.txt}" -i parts.txt
cat *.ts > andraday.ts
```
Also you can edit song names in chapter file and mux everything with mkvmerge.

### Sound problem fix
There is known sound stuttering problem with resulting ts files. To fix it remux file to mp4 and apply aac_adtstoasc bitstream filter:
```
ffmpeg -i v.ts -absf aac_adtstoasc -c copy out.mp4
```

### Note on ac3 muxing
Audio in ac3 stream can be slightly out of sync with ts. The best method is to extract first minute or so, find the exact delay (you can do it automatically and prescisely [with my other project](https://github.com/banteg/audos)), then fix ac3 with [delaycut](http://www.videohelp.com/software/delaycut) and finally mux with ffmpeg.

```
ffmpeg -i v.ts -t 60 v.wav
ffmpeg -i a.ac3 -t 60 a.wav
audos v.wav a.wav
delaycut
ffmpeg -i v.ts -i a_cut.ac3 -map 0:0 -map 0:1 -map 1 -absf aac_adtstoasc -c copy out.mp4
```
