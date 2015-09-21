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

To download 1080p performance of Take That through Tor, type:
```
itf 20 takethat -p 127.0.0.1:9050
```

To dump the urls for later use, type:
```
itf 19 andraday 720p --dump
```
Then you can download the parts somewhat like that:
```
aria2c -c -j 10 --header="Cookie: {token.txt}" -i parts.txt
cat *.ts > andraday.ts
```
