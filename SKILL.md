# YouTube AI Routine

Routine schedulata che cerca video YouTube per keyword configurabili,
ne estrae i sottotitoli (inglese e italiano) e salva ogni video come
file Markdown in `youtube-ai-routine/output/`.

## Come eseguirla

```bash
pip install -r youtube-ai-routine/requirements.txt
python3 youtube-ai-routine/routine.py
```

## Configurazione

Le keyword, il numero massimo di risultati per keyword e le lingue dei
sottotitoli si modificano direttamente nella sezione `CONFIGURAZIONE`
in cima a `youtube-ai-routine/routine.py`.

## Prerequisiti noti

- Richiede accesso di rete in uscita verso `www.youtube.com` e
  `*.googlevideo.com`. Se l'ambiente instrada il traffico attraverso un
  proxy con policy di allow-list, questi host vanno sbloccati
  esplicitamente: senza di essi la ricerca e il download dei sottotitoli
  falliscono con errori di connessione (es. `403 Forbidden` sul tunnel
  CONNECT) e la routine non produce alcun file.
- `yt-dlp` non è preinstallato nell'ambiente di esecuzione: va installato
  ad ogni run tramite `requirements.txt` finché non viene aggiunto un
  setup persistente (es. un hook `SessionStart`).
