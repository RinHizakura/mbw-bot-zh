# mbw-bot-zh

Search the official zh-Hant subtitles of Maebashi Witches (12 episodes, Ani-One's YouTube
channel) and play any line at its exact second in an embedded YouTube player.
Static site, no server.

## Layout

- `episodes.txt` – video IDs in episode order
- `subs/epNN_ID.vtt` – subtitles
- `build.py` – parses `subs/` into `docs/cues.json`
- `docs/` – the site: `index.html` + `cues.json` (committed; subs do not change)

## Local preview

```bash
python3 -m http.server -d docs 8001   # http://localhost:8001
```

## Re-fetch subtitles

```bash
pip install yt-dlp
yt-dlp --js-runtimes node -a episodes.txt --skip-download --write-subs --sub-lang zh-Hant \
  --sub-format vtt -o "subs/ep%(autonumber)02d_%(id)s"
for f in subs/*.zh-Hant.vtt; do mv "$f" "${f/.zh-Hant/}"; done   # drop the language suffix
python3 build.py
```
