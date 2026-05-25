# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the script

```bash
cd youtube-ai-routine
pip install yt-dlp
python routine.py
```

Output `.md` files are written to `youtube-ai-routine/output/` (created automatically).

## Architecture

Single-file script: `youtube-ai-routine/routine.py`

**Flow:**
1. For each keyword in `KEYWORDS`, call `search_youtube()` → returns a list of video dicts via `yt_dlp` flat extraction (no download)
2. Deduplicate videos by ID across all keywords
3. For each unique video, call `extract_subtitles()` twice (EN + IT) → downloads the `.vtt` file to a temp path, parses it with `parse_vtt()`, removes the temp file
4. `build_markdown()` assembles a `.md` document with video metadata and both transcriptions
5. `save_markdown()` writes it to `OUTPUT_DIR` with a `YYYY-MM-DD_<slug>.md` filename (adds a counter suffix on collision)

**Configuration constants** (top of `routine.py`):
- `KEYWORDS` — list of YouTube search terms
- `MAX_RESULTS` — videos fetched per keyword
- `OUTPUT_DIR` — output folder path (default `output`)
- `LANG_PRIMARY` / `LANG_SECONDARY` — subtitle languages (default `en` / `it`)

**Subtitle extraction** prefers human-authored subtitles over auto-generated ones; auto-generated transcriptions are prefixed with `*(auto-generated)*` in the output.
