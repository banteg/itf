## iTunes Festival London 2014 – Show Downloader

### Installation:
Install [Python 3](https://www.python.org/downloads/), launch terminal and type:
```
pip install itf
```

### Usage:
`itf` see this help

`itf shows` see shows available for download

`itf <day> <artist> [quality]` download specific show

### Options:
`quality` 1080p, 720p or ac3 (default: 1080p)

### Example:
To download AC3 audio stream for Kasabian, type
```
itf 05 20478838_kasabian ac3
```

### Note:
You can mux .ts and .ac3 with [mkvmerge](http://www.videohelp.com/tools/MKVtoolnix), but you'll need to adjust audio delay manually.

Thanks [tdragonite](https://github.com/tdragonite/) for original [bash script](https://gist.github.com/tdragonite/b084d4af4beefbde7ef9).
