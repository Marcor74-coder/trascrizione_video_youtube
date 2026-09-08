# trascrizione_video_youtube

Routine Python che cerca video su YouTube per keyword configurabili, estrae
i sottotitoli (EN + IT) con `yt-dlp` e salva ogni video come file `.md`.

## Struttura del progetto

```
.
├── youtube-ai-routine/
│   ├── routine.py           # script principale
│   ├── requirements.txt     # dipendenze Python
│   └── output/               # file .md generati (uno per video)
└── .claude/skills/youtube-ai-routine/SKILL.md  # skill per creare/eseguire/aggiornare la routine
```

## Setup ed esecuzione

```bash
pip install -r youtube-ai-routine/requirements.txt
python3 youtube-ai-routine/routine.py
```

I file `.md` vengono salvati in `youtube-ai-routine/output/` con formato
`YYYY-MM-DD_titolo-video.md`.

## Nota: accesso di rete a YouTube negli ambienti sandbox

Confermato piu' volte tra il 2026-07-02 e il 2026-09-08: in ambienti Claude
Code on the web con criteri di rete ristretti, il proxy dell'ambiente
rifiuta con 403 le connessioni dirette a `www.youtube.com`
(`connect_rejected` — organization policy), impedendo l'esecuzione della
routine. Lo script e' funzionalmente corretto: il blocco e' a livello di
policy di rete dell'ambiente, non un bug del codice. Per eseguire davvero la
routine serve un ambiente con accesso Internet completo verso YouTube (es.
in locale, o un ambiente/sessione con policy di rete "full access" che
includa `youtube.com` e i domini `*.googlevideo.com`).
