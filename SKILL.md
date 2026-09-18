---
name: youtube-ai-routine
description: Routine schedulata che cerca video YouTube per keyword configurabili (AI, Claude, LLM, ecc.), estrae i sottotitoli disponibili (inglese e italiano) e salva ogni video trovato come file Markdown in `youtube-ai-routine/output/`.
---

# YouTube AI Routine

Questa skill descrive come eseguire la routine di trascrizione video contenuta in questo repository.

## Cosa fa

Lo script `youtube-ai-routine/routine.py`:

1. Cerca su YouTube i video più recenti per ciascuna keyword definita in `KEYWORDS` (in cima al file).
2. Per ogni video trovato (deduplicato per ID), scarica i sottotitoli in inglese e in italiano, preferendo quelli caricati manualmente e usando quelli auto-generati come fallback.
3. Genera un file `.md` per video con titolo, URL, canale, data di pubblicazione, durata e le trascrizioni estratte.
4. Salva tutti i file nella cartella `youtube-ai-routine/output/` (creata automaticamente se non esiste), con nome `AAAA-MM-GG_titolo-slug.md`.

## Come eseguirla

Requisiti:

```bash
pip install -r youtube-ai-routine/requirements.txt
```

Esecuzione:

```bash
python3 youtube-ai-routine/routine.py
```

Non servono argomenti da riga di comando: le keyword, il numero massimo di risultati per keyword e le lingue dei sottotitoli si configurano modificando le costanti `KEYWORDS`, `MAX_RESULTS`, `OUTPUT_DIR`, `LANG_PRIMARY` e `LANG_SECONDARY` in cima a `routine.py`.

## Vincoli noti dell'ambiente

- Lo script dipende dal pacchetto Python `yt-dlp` (vedi `youtube-ai-routine/requirements.txt`); se non è già installato nell'ambiente di esecuzione, va installato prima di lanciare la routine.
- Lo script richiede accesso di rete in uscita verso `youtube.com` e i domini `*.googlevideo.com` (usati per scaricare i file dei sottotitoli). Se la policy di rete dell'ambiente blocca questi domini, la ricerca e l'estrazione falliranno con errori di connessione: in tal caso serve aggiornare la policy di rete della sessione/ambiente, non è un problema risolvibile nel codice.
