"""Copertine del podcast e degli episodi, generate gratis durante GitHub Actions.

Lo sfondo viene da Pollinations.ai (generatore di immagini gratuito, senza chiave);
la scritta "Rassegna Stampa" e la data vengono aggiunte con Pillow, perché i modelli
di immagini scrivono male i testi. Se Pollinations non risponde, si usa uno sfondo
grafico generato in locale: la copertina esce comunque.
"""
import hashlib
import random
import time
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = 1400  # Apple Podcasts richiede da 1400 a 3000 px, quadrata
MASTHEAD = "Rassegna Stampa"
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
        "agosto", "settembre", "ottobre", "novembre", "dicembre"]
GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]

STYLE = ("editorial illustration for a news podcast, symbolic and abstract, "
         "muted elegant colors, soft light, magazine cover art, "
         "no text, no letters, no words, no logos, no recognizable people")

SERIF = ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
         "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"]
SANS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"]


def _font(candidates, size):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def _seed(text: str) -> int:
    return int(hashlib.sha256(text.encode()).hexdigest()[:8], 16)


def _pollinations(prompt: str, seed: int):
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt)
           + f"?width={SIZE}&height={SIZE}&nologo=true&seed={seed}&model=flux")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "rassegna-podcast"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                img = Image.open(BytesIO(resp.read())).convert("RGB")
            return img.resize((SIZE, SIZE), Image.LANCZOS)
        except Exception as exc:  # noqa: BLE001
            print(f"  Pollinations tentativo {attempt + 1} fallito: {exc}")
            time.sleep(10 * (attempt + 1))
    return None


def _fallback(seed: int):
    """Sfondo astratto: gradiente con cerchi sfocati, colori decisi dal seed."""
    rnd = random.Random(seed)
    palettes = [((18, 32, 58), (196, 84, 52)), ((22, 48, 44), (214, 170, 72)),
                ((40, 24, 56), (88, 150, 196)), ((30, 30, 34), (180, 60, 70))]
    top, accent = rnd.choice(palettes)
    img = Image.new("RGB", (SIZE, SIZE), top)
    draw = ImageDraw.Draw(img)
    for y in range(SIZE):
        t = y / SIZE
        draw.line([(0, y), (SIZE, y)], fill=tuple(int(top[i] * (1 - t * .5)) for i in range(3)))
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for _ in range(7):
        r = rnd.randint(150, 450)
        x, y = rnd.randint(0, SIZE), rnd.randint(0, int(SIZE * .7))
        ld.ellipse([x - r, y - r, x + r, y + r], fill=accent + (rnd.randint(40, 110),))
    layer = layer.filter(ImageFilter.GaussianBlur(60))
    img.paste(layer, (0, 0), layer)
    return img


def _shade(img, start: float):
    """Scurisce la parte bassa dell'immagine per rendere leggibile il testo."""
    grad = Image.new("L", (1, SIZE))
    for y in range(SIZE):
        t = max(0.0, (y / SIZE - start) / (1 - start))
        grad.putpixel((0, y), int(235 * min(1.0, t * 1.3)))
    alpha = grad.resize((SIZE, SIZE))
    black = Image.new("RGB", (SIZE, SIZE), (8, 10, 14))
    return Image.composite(black, img, alpha)


def _text(draw, xy, text, font, fill=(255, 255, 255), anchor="ls"):
    x, y = xy
    draw.text((x + 3, y + 3), text, font=font, fill=(0, 0, 0), anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)


def podcast_cover(out: Path) -> None:
    seed = 2026
    prompt = ("stack of folded newspapers and a vintage microphone at dawn, "
              "warm sunrise light, " + STYLE)
    img = _pollinations(prompt, seed) or _fallback(seed)
    img = _shade(img, 0.35)
    draw = ImageDraw.Draw(img)
    margin = 100
    _text(draw, (margin, SIZE - 330), "Rassegna", _font(SERIF, 210))
    _text(draw, (margin, SIZE - 120), "Stampa", _font(SERIF, 210))
    draw.rectangle([margin, SIZE - 545, margin + 260, SIZE - 533], fill=(214, 64, 52))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "JPEG", quality=88)


def episode_cover(day, summary: str, out: Path) -> None:
    seed = _seed(day.isoformat())
    prompt = f"Temi del giorno: {summary}. " + STYLE
    img = _pollinations(prompt[:900], seed) or _fallback(seed)
    img = _shade(img, 0.55)
    draw = ImageDraw.Draw(img)
    margin = 90
    data = f"{GIORNI[day.weekday()]} {day.day} {MESI[day.month - 1]} {day.year}"
    draw.rectangle([margin, SIZE - 250, margin + 180, SIZE - 240], fill=(214, 64, 52))
    _text(draw, (margin, SIZE - 150), MASTHEAD, _font(SERIF, 120))
    _text(draw, (margin, SIZE - 75), data.capitalize(), _font(SANS, 58), fill=(225, 225, 225))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "JPEG", quality=88)
