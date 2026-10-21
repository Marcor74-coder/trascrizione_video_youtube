#!/usr/bin/env python3
"""
YouTube AI Routine
------------------
Cerca video su YouTube per keyword configurabili,
estrae i sottotitoli (EN + IT) e salva ogni video come file .md.
"""

import os
import re
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import yt_dlp

# ─────────────────────────────────────────────
# CONFIGURAZIONE — modifica questi valori
# ─────────────────────────────────────────────
KEYWORDS = [
    "artificial intelligence",
    "AI news",
    "large language models",
    "Claude",
]
MAX_RESULTS = 20          # video per keyword
OUTPUT_DIR = "output"     # cartella di output
LANG_PRIMARY = "en"       # lingua principale sottotitoli
LANG_SECONDARY = "it"     # lingua secondaria sottotitoli
# ─────────────────────────────────────────────


def sanitize_filename(title: str) -> str:
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    title = title.replace(" ", "-").lower()
    return title[:80]


def search_youtube(keyword: str, max_results: int) -> list[dict]:
    """Cerca video YouTube usando yt-dlp (non richiede API key)."""
    print(f"🔍 Ricerca: '{keyword}' (max {max_results} video)...")
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
        "nocheckcertificate": True,
    }
    query = f"ytsearch{max_results}:{keyword}"
    videos = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            for entry in info.get("entries", []):
                if not entry:
                    continue
                vid_id = entry.get("id", "")
                videos.append({
                    "id": vid_id,
                    "title": entry.get("title", "Senza titolo"),
                    "url": f"https://www.youtube.com/watch?v={vid_id}",
                    "channel": entry.get("uploader") or entry.get("channel", "Sconosciuto"),
                    "published": entry.get("upload_date", ""),
                    "duration": str(entry.get("duration", "")),
                })
        except Exception as e:
            print(f"  ⚠️  Errore ricerca '{keyword}': {e}")
    return videos


def extract_subtitles(video_url: str, lang: str) -> str:
    """
    Scarica i sottotitoli in una lingua specifica.
    Prova prima quelli umani, poi gli auto-generati.
    """
    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": [lang],
        "subtitlesformat": "vtt",
        "outtmpl": "/tmp/yt_sub_%(id)s",
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            video_id = info.get("id", "")

            subs = info.get("subtitles", {})
            auto_subs = info.get("automatic_captions", {})
            is_auto = False

            if lang in subs:
                source = subs[lang]
            elif lang in auto_subs:
                source = auto_subs[lang]
                is_auto = True
            else:
                return ""

            vtt_url = next(
                (s["url"] for s in source if s.get("ext") == "vtt"),
                source[0].get("url", "") if source else ""
            )
            if not vtt_url:
                return ""

            vtt_path = f"/tmp/yt_sub_{video_id}_{lang}.vtt"
            urllib.request.urlretrieve(vtt_url, vtt_path)

            text = parse_vtt(vtt_path)
            os.remove(vtt_path)

            if is_auto:
                text = "*(auto-generated)*\n\n" + text
            return text

        except Exception as e:
            print(f"  ⚠️  Sottotitoli {lang} non disponibili: {e}")
            return ""


def parse_vtt(vtt_path: str) -> str:
    with open(vtt_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    content = re.sub(r"WEBVTT.*?\n\n", "", content, flags=re.DOTALL)
    content = re.sub(r"\d{2}:\d{2}:\d{2}[.,]\d{3} --> .*\n", "", content)
    content = re.sub(r"<[^>]+>", "", content)
    content = re.sub(r"^\d+\s*$", "", content, flags=re.MULTILINE)
    content = re.sub(r"\n{3,}", "\n\n", content)

    lines = content.strip().split("\n")
    deduped = []
    prev = None
    for line in lines:
        if line.strip() != prev:
            deduped.append(line)
            prev = line.strip()

    return "\n".join(deduped).strip()


def build_markdown(video: dict, keyword: str, text_en: str, text_it: str) -> str:
    date_str = datetime.now().strftime("%Y-%m-%d")
    en_section = text_en if text_en else "Sottotitoli non disponibili."
    it_section = text_it if text_it else "Non disponibile."

    return f"""# {video['title']}

- **URL**: {video['url']}
- **Canale**: {video['channel']}
- **Data pubblicazione**: {video['published']}
- **Durata**: {video['duration']}
- **Keywords usate**: {keyword}
- **Estratto il**: {date_str}

---

## Trascrizione (English)

{en_section}

---

## Trascrizione (Italiano)

{it_section}
"""


def save_markdown(content: str, title: str, output_dir: str) -> str:
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = sanitize_filename(title)
    filename = f"{date_str}_{slug}.md"
    filepath = Path(output_dir) / filename

    counter = 1
    while filepath.exists():
        filepath = Path(output_dir) / f"{date_str}_{slug}_{counter}.md"
        counter += 1

    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    seen_ids = set()
    total_saved = 0

    for keyword in KEYWORDS:
        videos = search_youtube(keyword, MAX_RESULTS)

        for video in videos:
            vid_id = video["id"]
            if vid_id in seen_ids:
                continue
            seen_ids.add(vid_id)

            print(f"  📄 {video['title'][:60]}...")

            text_en = extract_subtitles(video["url"], LANG_PRIMARY)
            text_it = extract_subtitles(video["url"], LANG_SECONDARY)

            md_content = build_markdown(video, keyword, text_en, text_it)
            filepath = save_markdown(md_content, video["title"], OUTPUT_DIR)
            print(f"  ✅ Salvato: {filepath}")

            total_saved += 1
            time.sleep(1)

    print(f"\n🎉 Routine completata. {total_saved} file .md salvati in '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    main()
