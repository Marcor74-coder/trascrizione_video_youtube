# YouTube AI Routine

Routine schedulata che cerca video YouTube per keyword configurabili, ne estrae
i sottotitoli (inglese e italiano) e salva ogni video come file Markdown.

## Come eseguirla

1. Installa le dipendenze:
   ```
   pip install -r youtube-ai-routine/requirements.txt
   ```
2. Esegui lo script:
   ```
   python3 youtube-ai-routine/routine.py
   ```
3. I file `.md` prodotti vengono salvati in `youtube-ai-routine/output/`,
   uno per video, con nome `AAAA-MM-GG_titolo-slug.md`.

## Configurazione

Le keyword di ricerca, il numero massimo di risultati per keyword e le lingue
dei sottotitoli si modificano direttamente in cima a
`youtube-ai-routine/routine.py` (variabili `KEYWORDS`, `MAX_RESULTS`,
`LANG_PRIMARY`, `LANG_SECONDARY`).

## Requisiti ambientali

- `yt-dlp` deve essere installato (vedi `youtube-ai-routine/requirements.txt`).
- L'ambiente di esecuzione deve poter raggiungere `youtube.com` e i domini
  `*.googlevideo.com` usati per scaricare i sottotitoli. Se la policy di rete
  della sessione blocca questi domini, la routine non può completare la
  ricerca né l'estrazione dei sottotitoli.
