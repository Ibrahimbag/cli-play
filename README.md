# CLI-PLAY

![demo](demo.png)

A simple command-line video player written in Python. \
This is a more colorful and simple but badly optimized version of my previous project [bad-cli](https://github.com/Ibrahimbag/bad-cli).

## Installation

### Linux

```bash
sudo apt install python3 python3-pip git && \
pip install ffpyplayer numpy pymediainfo && \
git clone https://github.com/Ibrahimbag/cli-play.git && \
cd cli-play
```

## Usage

```bash
python3 cli-play.py [FILE_PATH]
```

## Known Issues

1. Audio becomes choppy and video delays when resolution of terminal is high.
