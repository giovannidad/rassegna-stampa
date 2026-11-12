"""Copertine del podcast e degli episodi, generate gratis durante GitHub Actions.

Lo sfondo è disegnato da SD-Turbo, un modello open source di generazione di immagini
che gira sul processore della macchina di GitHub: nessun account, nessuna chiave,
nessun costo. La scritta "Rassegna Stampa" e la data vengono aggiunte con Pillow,
perché i modelli di immagini scrivono male i testi. Se la generazione fallisce si usa
uno sfondo grafico di riserva: la copertina esce comunque.
"""
import hashlib
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = 1400  # Apple Podcasts richiede da 1400 a 3000 px, quadrata
MASTHEAD = "Rassegna Stampa"
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
        "agosto", "settembre", "ottobre", "novembre", "dicembre"]
GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]

STYLE = ("editorial magazine cover illustration, symbolic still life, objects only, "
         "elegant composition, muted colors, soft cinematic light, highly detailed")
DEFAULT_EPISODE = "a folded newspaper on a desk next to a cup of coffee at sunrise"

SERIF = ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
         "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"]
SANS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"]

_PIPE = None


def _font(candidates, size):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def _seed(text: str) -> int:
    return int(hashlib.sha256(text.encode()).hexdigest()[:8], 16)


def _generate(prompt: str, seed: int):
    global _PIPE
    try:
        import torch
        from diffusers import AutoPipelineForText2Image

        if _PIPE is None:
            torch.set_num_threads(max(1, (__import__("os").cpu_count() or 2)))
            _PIPE = AutoPipelineForText2Image.from_pretrained(
                "stabilityai/sd-turbo", torch_dtype=torch.float32)
            _PIPE.set_progress_bar_config(disable=True)
        gen = torch.Generator("cpu").manual_seed(seed)
        img = _PIPE(prompt=prompt, num_inference_steps=4, guidance_scale=0.0,
                    width=512, height=512, generator=gen).images[0]
        img = img.resize((SIZE, SIZE), Image.LANCZOS)
        return img.filter(ImageFilter.UnsharpMask(radius=2, percent=60))
    except Exception as exc:  # noqa: BLE001
        print(f"  generazione immagine non riuscita: {exc}")
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
    prompt = ("a vintage radio microphone in front of a stack of folded newspapers, "
              "warm sunrise light through a window, " + STYLE)
    img = _generate(prompt, seed) or _fallback(seed)
    img = _shade(img, 0.35)
    draw = ImageDraw.Draw(img)
    margin = 100
    _text(draw, (margin, SIZE - 330), "Rassegna", _font(SERIF, 210))
    _text(draw, (margin, SIZE - 120), "Stampa", _font(SERIF, 210))
    draw.rectangle([margin, SIZE - 545, margin + 260, SIZE - 533], fill=(214, 64, 52))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "JPEG", quality=88)


def episode_cover(day, scene: str, out: Path) -> None:
    seed = _seed(day.isoformat())
    prompt = f"{scene or DEFAULT_EPISODE}, {STYLE}"
    img = _generate(prompt, seed) or _fallback(seed)
    img = _shade(img, 0.55)
    draw = ImageDraw.Draw(img)
    margin = 90
    data = f"{GIORNI[day.weekday()]} {day.day} {MESI[day.month - 1]} {day.year}"
    draw.rectangle([margin, SIZE - 250, margin + 180, SIZE - 240], fill=(214, 64, 52))
    _text(draw, (margin, SIZE - 150), MASTHEAD, _font(SERIF, 120))
    _text(draw, (margin, SIZE - 75), data.capitalize(), _font(SANS, 58), fill=(225, 225, 225))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "JPEG", quality=88)
