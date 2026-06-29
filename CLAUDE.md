# trascrizione_video_youtube

Routine Python che cerca video su YouTube per keyword configurabili,
estrae i sottotitoli (EN + IT) con yt-dlp e salva ogni video come file `.md`.

## Struttura del progetto

```
.
├── youtube-ai-routine/routine.py       # script principale
├── requirements.txt                    # dipendenze Python
├── output/                             # file .md generati (uno per video)
└── .claude/skills/youtube-ai-routine/  # skill Claude Code per rigenerare/aggiornare la routine
```

## Setup

```bash
pip install -r requirements.txt
```

## Utilizzo

```bash
python youtube-ai-routine/routine.py
```

I file `.md` vengono salvati in `output/` con formato:
`YYYY-MM-DD_titolo-video.md`

## Configurazione

Modifica le costanti in cima a `youtube-ai-routine/routine.py`:

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `KEYWORDS` | `["artificial intelligence", ...]` | Keyword di ricerca |
| `MAX_RESULTS` | `20` | Video per keyword |
| `OUTPUT_DIR` | `"output"` | Cartella di destinazione |
| `LANG_PRIMARY` | `"en"` | Lingua principale sottotitoli |
| `LANG_SECONDARY` | `"it"` | Lingua secondaria |

## Esecuzione periodica (cron)

```bash
# ogni giorno alle 8:00
0 8 * * * cd /path/to/trascrizione_video_youtube && python youtube-ai-routine/routine.py
```

## Skill Claude Code

La skill `.claude/skills/youtube-ai-routine/` permette di rigenerare o
aggiornare la routine con `/youtube-ai-routine` da Claude Code.
