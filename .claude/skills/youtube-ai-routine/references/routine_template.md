# Template: routine.py

Questo è il template completo dello script Python da creare.
Claude Code deve usarlo come base, sostituendo `KEYWORDS` con quelle dell'utente.

```python
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
import json
from datetime import datetime
from pathlib import Path

import yt_dlp
from youtubesearchpython import VideosSearch

# ─────────────────────────────────────────────
# CONFIGURAZIONE — modifica questi valori
# ─────────────────────────────────────────────
KEYWORDS = ["artificial intelligence", "AI news"]  # <-- keyword configurabili
MAX_RESULTS = 20          # video per keyword
OUTPUT_DIR = "output"     # cartella di output
LANG_PRIMARY = "en"       # lingua principale sottotitoli
LANG_SECONDARY = "it"     # lingua secondaria sottotitoli
# ─────────────────────────────────────────────


def sanitize_filename(title: str) -> str:
    """Rimuove caratteri non validi per i nomi file."""
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    title = title.replace(" ", "-").lower()
    return title[:80]  # tronca a 80 caratteri


def search_youtube(keyword: str, max_results: int) -> list[dict]:
    """Cerca video YouTube per keyword e restituisce metadati."""
    print(f"🔍 Ricerca: '{keyword}' (max {max_results} video)...")
    search = VideosSearch(keyword, limit=max_results)
    results = search.result()
    videos = []
    for item in results.get("result", []):
        videos.append({
            "id": item.get("id", ""),
            "title": item.get("title", "Senza titolo"),
            "url": item.get("link", ""),
            "channel": item.get("channel", {}).get("name", "Sconosciuto"),
            "published": item.get("publishedTime", ""),
            "duration": item.get("duration", ""),
        })
    return videos


def extract_subtitles(video_url: str, lang: str) -> str:
    """
    Scarica i sottotitoli di un video in una lingua specifica.
    Prova prima i sottotitoli umani, poi quelli auto-generati.
    Restituisce il testo pulito o stringa vuota se non disponibili.
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
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            video_id = info.get("id", "")

            # Controlla sottotitoli umani
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

            # Scarica il file vtt
            vtt_url = next(
                (s["url"] for s in source if s.get("ext") == "vtt"),
                source[0].get("url", "") if source else ""
            )
            if not vtt_url:
                return ""

            import urllib.request
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
    """Converte un file .vtt in testo pulito senza tag temporali."""
    with open(vtt_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Rimuovi header WEBVTT
    content = re.sub(r"WEBVTT.*?\n\n", "", content, flags=re.DOTALL)
    # Rimuovi timestamp lines (es. 00:00:01.000 --> 00:00:03.000)
    content = re.sub(r"\d{2}:\d{2}:\d{2}[.,]\d{3} --> .*\n", "", content)
    # Rimuovi tag HTML (<c>, <b>, ecc.)
    content = re.sub(r"<[^>]+>", "", content)
    # Rimuovi righe con solo numeri (indici cue)
    content = re.sub(r"^\d+\s*$", "", content, flags=re.MULTILINE)
    # Rimuovi righe vuote multiple
    content = re.sub(r"\n{3,}", "\n\n", content)

    # Deduplicazione righe consecutive identiche (comune nei VTT)
    lines = content.strip().split("\n")
    deduped = []
    prev = None
    for line in lines:
        if line.strip() != prev:
            deduped.append(line)
            prev = line.strip()

    return "\n".join(deduped).strip()


def build_markdown(video: dict, keyword: str, text_en: str, text_it: str) -> str:
    """Costruisce il contenuto Markdown per un video."""
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
    """Salva il contenuto .md su file e restituisce il percorso."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = sanitize_filename(title)
    filename = f"{date_str}_{slug}.md"
    filepath = Path(output_dir) / filename

    # Evita sovrascrittura
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
                continue  # evita duplicati tra keyword diverse
            seen_ids.add(vid_id)

            print(f"  📄 {video['title'][:60]}...")

            text_en = extract_subtitles(video["url"], LANG_PRIMARY)
            text_it = extract_subtitles(video["url"], LANG_SECONDARY)

            md_content = build_markdown(video, keyword, text_en, text_it)
            filepath = save_markdown(md_content, video["title"], OUTPUT_DIR)
            print(f"  ✅ Salvato: {filepath}")

            total_saved += 1
            time.sleep(1)  # evita rate limiting

    print(f"\n🎉 Routine completata. {total_saved} file .md salvati in '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    main()
```

---

## Note per Claude Code

- Lo script va salvato come `routine.py` nella directory di lavoro dell'utente.
- Prima di eseguirlo, verifica con `pip show yt-dlp youtube-search-python` che
  le dipendenze siano installate.
- Se l'utente è su Windows, il path `/tmp/` non esiste: sostituisci con
  `os.path.join(os.environ.get('TEMP', '.'), ...)`.
- Per uso periodico, suggerisci all'utente di aggiungere a crontab:
  `0 8 * * * cd /path/to/routine && python routine.py`
