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

`-d or --dump` dump token and parts instead of downloading, combine with `-c` to skip downloading and save chapters

`-c or --chapters` save chapters file, note that you'll need to add song names manually and then mux it (see below)

`-j or --threads` select number of download threads (1–1000, default: 20)

### Examples
To download The Chemical Brothers in 1080p, type:
```
itf 24 thechemicalbrothers
```

To download 6-channel audio for Pharrell Williams, type:
```
itf 26 pharrellwilliams ac3
```

To dump chapters of Take That via Tor, type:
```
itf 20 takethat --dump --chapters -p 127.0.0.1:9050
```

### Notes
Complete list of concerts [is here](https://github.com/banteg/itf/issues/3#issuecomment-142756300).

It might be a good idea to remux `.ts` file to `.mp4`, use [Yamb](http://www.videohelp.com/software/YAMB) (on Windows) or [Subler](http://videohelp.com/software/Subler) (on Mac), don't use ffmpeg.

You may want to edit song names in chapter file and mux everything with with Yamb or Subler.

Audio in `.ac3` stream might be slightly out of sync. Delay/rush can be fixed with [delaycut](http://www.videohelp.com/software/delaycut).
