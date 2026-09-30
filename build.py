#!/usr/bin/env python3
"""Parse subs/*.vtt into docs/cues.json for the GitHub Pages site. Run after re-fetching subs."""
import glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def to_sec(ts):  # "00:01:02.345" -> 62.345
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def cues():
    """Yield (ep, video_id, start_sec, text) for every cue in subs/*.vtt."""
    for f in sorted(glob.glob(os.path.join(HERE, "subs", "*.vtt"))):
        ep, vid = re.search(r"ep(\d+)_([\w-]{11})", f).groups()
        start, buf = None, []
        for line in open(f, encoding="utf-8").read().splitlines() + [""]:
            if "-->" in line:
                start = to_sec(line.split(" --> ")[0])
            elif line.strip():
                buf.append(line.strip())
            elif start is not None and buf:  # blank line ends the cue
                yield int(ep), vid, start, " ".join(buf)
                start, buf = None, []


if __name__ == "__main__":
    rows = [[ep, vid, round(sec, 1), text] for ep, vid, sec, text in cues()]
    assert to_sec("00:01:02.500") == 62.5 and len({r[0] for r in rows}) == 12 and len(rows) > 6000
    out = os.path.join(HERE, "docs", "cues.json")
    json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"{len(rows)} cues -> {out}")
