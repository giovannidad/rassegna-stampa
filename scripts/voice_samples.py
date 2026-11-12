"""Genera un campione audio per ogni voce italiana disponibile (Edge TTS e Piper)."""
import asyncio
import subprocess
import urllib.request
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "samples"
TEXT = ("Buongiorno, è giovedì 12 novembre. Ecco la rassegna stampa. "
        "L'Agenzia per la Cybersicurezza Nazionale ha segnalato una vulnerabilità critica "
        "che riguarda anche i sistemi della pubblica amministrazione. "
        "Passiamo alla privacy: il Garante ha pubblicato nuove indicazioni per i Comuni.")

PIPER = ["it_IT-paola-medium", "it_IT-riccardo-x_low"]


async def edge():
    voices = [v for v in await edge_tts.list_voices() if v["Locale"] == "it-IT"]
    for v in voices:
        name = v["ShortName"]
        await edge_tts.Communicate(TEXT, name, rate="+5%").save(str(OUT / f"edge_{name}.mp3"))
        print(f"Edge: {name} ({v['Gender']})")


def piper():
    for voice in PIPER:
        lang, rest = voice.split("-", 1)
        speaker, quality = rest.rsplit("-", 1)
        base = (f"https://huggingface.co/rhasspy/piper-voices/resolve/main/"
                f"it/{lang}/{speaker}/{quality}/{voice}")
        for ext in (".onnx", ".onnx.json"):
            urllib.request.urlretrieve(base + ext, f"/tmp/{voice}{ext}")
        wav = Path(f"/tmp/{voice}.wav")
        subprocess.run(["piper", "--model", f"/tmp/{voice}.onnx", "--output_file", str(wav)],
                       input=TEXT.encode(), check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ac", "1",
                        "-b:a", "64k", str(OUT / f"piper_{voice}.mp3")], check=True)
        print(f"Piper: {voice}")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    asyncio.run(edge())
    piper()
