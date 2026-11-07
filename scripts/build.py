#!/usr/bin/env python3
"""Genera gli MP3 dai copioni in episodes/ e ricostruisce docs/feed.xml.

Ogni copione è un file episodes/AAAA-MM-GG.md con questo formato:

    ---
    title: Rassegna del 9 novembre
    summary: Una riga con i temi principali.
    sources:
      - name: ANSA
        url: https://www.ansa.it/...
    ---
    Testo da leggere ad alta voce...
"""
import asyncio
import datetime as dt
import html
import os
import subprocess
import sys
import urllib.request
from email.utils import format_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parent.parent
EPISODES = ROOT / "episodes"
DOCS = ROOT / "docs"
AUDIO = DOCS / "audio"
VOICES = ROOT / ".voices"
TZ = ZoneInfo("Europe/Rome")

CFG = yaml.safe_load((ROOT / "config.yml").read_text(encoding="utf-8"))


def base_url() -> str:
    if os.environ.get("BASE_URL"):
        return os.environ["BASE_URL"].rstrip("/") + "/"
    repo = os.environ.get("GITHUB_REPOSITORY", "utente/rassegna")
    owner, name = repo.split("/")
    return f"https://{owner.lower()}.github.io/{name}/"


def parse(path: Path):
    raw = path.read_text(encoding="utf-8")
    meta, body = {}, raw
    if raw.startswith("---"):
        _, fm, body = raw.split("---", 2)
        meta = yaml.safe_load(fm) or {}
    return meta, body.strip()


def tts_edge(text: str, out: Path) -> None:
    import edge_tts

    async def run():
        com = edge_tts.Communicate(text, CFG["edge_voice"], rate=CFG.get("edge_rate", "+0%"))
        await com.save(str(out))

    asyncio.run(run())
    if not out.exists() or out.stat().st_size < 10_000:
        raise RuntimeError("Edge TTS ha prodotto un file vuoto")


def tts_piper(text: str, out: Path) -> None:
    voice = CFG["piper_voice"]
    lang, rest = voice.split("-", 1)
    speaker, quality = rest.rsplit("-", 1)
    family = lang.split("_")[0]
    VOICES.mkdir(exist_ok=True)
    model = VOICES / f"{voice}.onnx"
    base = (f"https://huggingface.co/rhasspy/piper-voices/resolve/main/"
            f"{family}/{lang}/{speaker}/{quality}/{voice}")
    for ext in (".onnx", ".onnx.json"):
        target = VOICES / f"{voice}{ext}"
        if not target.exists():
            urllib.request.urlretrieve(base + ext, target)
    wav = out.with_suffix(".wav")
    subprocess.run(["piper", "--model", str(model), "--output_file", str(wav)],
                   input=text.encode("utf-8"), check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
                    "-ac", "1", "-b:a", "64k", str(out)], check=True)
    wav.unlink()


def duration(path: Path) -> int:
    res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(path)],
                         capture_output=True, text=True)
    try:
        return int(float(res.stdout.strip()))
    except ValueError:
        return 0


def synthesize(md: Path) -> None:
    mp3 = AUDIO / f"{md.stem}.mp3"
    if mp3.exists():
        return
    _, body = parse(md)
    try:
        tts_edge(body, mp3)
        print(f"{md.stem}: audio generato con Edge TTS")
    except Exception as exc:  # noqa: BLE001
        print(f"{md.stem}: Edge TTS non disponibile ({exc}), uso Piper", file=sys.stderr)
        mp3.unlink(missing_ok=True)
        tts_piper(body, mp3)
        print(f"{md.stem}: audio generato con Piper")


def prune(files):
    keep = CFG.get("keep_episodes", 30)
    for md in files[:-keep] if len(files) > keep else []:
        md.unlink()
        (AUDIO / f"{md.stem}.mp3").unlink(missing_ok=True)
    return files[-keep:]


def build_feed(files) -> None:
    url = base_url()
    items = []
    for md in reversed(files):
        mp3 = AUDIO / f"{md.stem}.mp3"
        if not mp3.exists():
            continue
        meta, _ = parse(md)
        day = dt.date.fromisoformat(md.stem)
        pub = dt.datetime.combine(day, dt.time(6, 30), TZ)
        title = meta.get("title") or f"Rassegna del {day.strftime('%d/%m/%Y')}"
        summary = meta.get("summary", "")
        sources = meta.get("sources") or []
        desc = f"<p>{html.escape(summary)}</p>"
        if sources:
            desc += "<p>Fonti:</p><ul>" + "".join(
                f'<li><a href="{html.escape(s.get("url", ""))}">{html.escape(s.get("name", ""))}</a></li>'
                for s in sources) + "</ul>"
        items.append(f"""    <item>
      <title>{html.escape(title)}</title>
      <description><![CDATA[{desc}]]></description>
      <itunes:summary>{html.escape(summary)}</itunes:summary>
      <enclosure url="{url}audio/{mp3.name}" length="{mp3.stat().st_size}" type="audio/mpeg"/>
      <guid isPermaLink="false">rassegna-{md.stem}</guid>
      <pubDate>{format_datetime(pub)}</pubDate>
      <itunes:duration>{duration(mp3)}</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
    </item>""")

    now = format_datetime(dt.datetime.now(TZ))
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{html.escape(CFG['title'])}</title>
    <link>{url}</link>
    <atom:link href="{url}feed.xml" rel="self" type="application/rss+xml"/>
    <description>{html.escape(CFG['description'])}</description>
    <language>{CFG['language']}</language>
    <lastBuildDate>{now}</lastBuildDate>
    <itunes:author>{html.escape(CFG['author'])}</itunes:author>
    <itunes:explicit>false</itunes:explicit>
    <itunes:block>Yes</itunes:block>
    <itunes:category text="News"/>
{chr(10).join(items)}
  </channel>
</rss>
"""
    (DOCS / "feed.xml").write_text(feed, encoding="utf-8")
    (DOCS / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (DOCS / "index.html").write_text(
        '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex">'
        f"<title>{html.escape(CFG['title'])}</title>"
        f'<p>Feed privato: <a href="feed.xml">feed.xml</a></p>', encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    AUDIO.mkdir(parents=True, exist_ok=True)
    files = sorted(EPISODES.glob("????-??-??.md"))
    files = prune(files)
    for md in files:
        synthesize(md)
    build_feed(files)
    print(f"Feed aggiornato: {base_url()}feed.xml ({len(files)} episodi)")


if __name__ == "__main__":
    main()
