# Skill: YouTube AI Transcription Routine

## Scopo

Questa routine cerca video YouTube su temi di intelligenza artificiale, estrae i sottotitoli (EN + IT) e salva ogni video come file `.md` nella cartella `youtube-ai-routine/output/`.

## Istruzioni per la routine schedulata

### 1. Installa le dipendenze

```bash
pip install yt-dlp
```

### 2. Esegui lo script

```bash
cd youtube-ai-routine
python routine.py
```

### 3. Salva i risultati

Se lo script produce file `.md` nella cartella `output/`:

1. Fai `git add` dei nuovi file
2. Fai commit con messaggio `[routine] Add transcriptions YYYY-MM-DD`
3. Fai push sul branch corrente

### 4. Invia notifica

Al termine, invia una notifica con:
- Numero di file `.md` generati
- Keywords utilizzate
- Eventuali errori riscontrati

Se lo script fallisce (es. modulo mancante, errore di rete), invia comunque una notifica con la descrizione dell'errore.

## Keyword monitorate

- artificial intelligence
- AI news
- large language models
- Claude
- Claude Code
- Routine
- NotebookLM
- ChatGPT

## Output

Ogni file `.md` contiene:
- Titolo, URL, canale, data, durata del video
- Trascrizione in inglese (se disponibile)
- Trascrizione in italiano (se disponibile)

## Note

- I video già processati vengono saltati (deduplicazione per ID)
- Se i sottotitoli non sono disponibili, il campo viene lasciato vuoto
- I sottotitoli auto-generati sono marcati con `*(auto-generated)*`
