---
name: youtube-ai-routine
description: "Cerca su YouTube i video più recenti per una lista di keyword configurabili, estrae i sottotitoli (inglese e italiano) e salva ogni video trovato come file Markdown in youtube-ai-routine/output/. Usa questa skill quando il compito schedulato chiede di eseguire la routine YouTube AI o di aggiornare la raccolta di trascrizioni."
---

## Cosa fa questa routine

Lo script `youtube-ai-routine/routine.py` automatizza la raccolta di trascrizioni da YouTube:

1. Per ogni keyword in `KEYWORDS` (dentro `routine.py`), cerca i primi `MAX_RESULTS` video su YouTube.
2. Per ogni video nuovo (deduplicato per ID), scarica i sottotitoli in inglese (`LANG_PRIMARY`) e italiano (`LANG_SECONDARY`), preferendo i sottotitoli umani e ripiegando su quelli auto-generati.
3. Genera un file `.md` per video con: titolo, URL, canale, data di pubblicazione, durata, keyword usata, data di estrazione, trascrizione EN e trascrizione IT.
4. Salva il file in `youtube-ai-routine/output/` con nome `YYYY-MM-DD_titolo-slug.md` (gestendo le collisioni con un suffisso numerico).

## Come eseguirla

Prerequisito: la libreria `yt-dlp` deve essere installata (`pip install -r youtube-ai-routine/requirements.txt`).

```bash
cd youtube-ai-routine
python3 routine.py
```

Lo script crea la cartella `output/` se non esiste e stampa un log dei video trovati/salvati. Non richiede argomenti né input interattivo.

## Quando usarla

- Quando un task schedulato dice di "eseguire la routine YouTube AI" o fa riferimento a questa skill.
- Quando l'utente chiede di aggiornare/rigenerare la raccolta di trascrizioni YouTube per le keyword configurate.

## Note operative

- Le keyword, il numero massimo di risultati e le lingue dei sottotitoli si modificano direttamente nelle costanti in cima a `routine.py`.
- La ricerca usa `ytsearch{N}:{keyword}` via `yt_dlp`; non serve una API key di YouTube.
- Ogni video viene processato una sola volta per run (deduplica in memoria tramite `seen_ids`); rilanciare lo script rigenera comunque i video già salvati in precedenza (non c'è deduplica persistente tra run diversi), a meno che non venga aggiunta una cache esterna.
- Se i sottotitoli non sono disponibili in una lingua, il file Markdown riporta "Sottotitoli non disponibili." (EN) o "Non disponibile." (IT) al posto della trascrizione.

## Vincoli ambientali noti

- In una sessione Claude Code on the web, `yt-dlp` non è preinstallato: va installato manualmente (`pip install -r youtube-ai-routine/requirements.txt`) oppure tramite un hook `SessionStart` configurato interattivamente da un utente umano (la creazione dell'hook non è consentita in run automatici/non presidiati — vedi skill `session-start-hook`).
- L'accesso di rete a `youtube.com` e ai domini `*.googlevideo.com` può essere bloccato dalla policy di rete dell'ambiente/sessione (proxy con `403 Forbidden` sul CONNECT). Se la routine fallisce con errori di connessione/proxy, la policy di rete dell'ambiente va aggiornata da un utente umano prima di rilanciarla: non è un problema risolvibile via codice.
