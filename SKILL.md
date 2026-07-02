# Skill: YouTube AI Transcription Routine

## Scopo

Questa routine cerca su YouTube video recenti sui temi AI monitorati, estrae i
sottotitoli (EN + IT) con `yt-dlp` e salva ogni video come file `.md`
individuale in `youtube-ai-routine/output/`.

## Istruzioni per la routine schedulata

1. **Installa le dipendenze** (l'ambiente remoto non le ha preinstallate):
   ```bash
   pip install -r youtube-ai-routine/requirements.txt
   ```
2. **Esegui lo script**:
   ```bash
   cd youtube-ai-routine
   python routine.py
   ```
3. **Salva i risultati**: se lo script produce nuovi file `.md` in `output/`,
   fai `git add`, commit (`[routine] Add transcriptions YYYY-MM-DD`) e push
   sul branch di lavoro della sessione.
4. **Notifica** l'esito: numero di file generati, keyword usate ed eventuali
   errori. Se lo script fallisce, notifica comunque con la descrizione
   dell'errore invece di ripetere il setup da zero.

## Keyword monitorate

- artificial intelligence
- AI news
- large language models
- Claude
- Claude Code
- NotebookLM
- ChatGPT

## Nota importante — accesso di rete

Questa routine richiede di raggiungere `www.youtube.com` (ricerca) e i domini
CDN dei sottotitoli. Se l'ambiente di esecuzione applica una policy di rete
allowlist, questi domini devono essere abilitati esplicitamente nelle
impostazioni dell'ambiente (Claude Code on the web), altrimenti ogni
esecuzione fallirà con un errore di connessione/proxy indipendentemente da
questo file.

## Note

- I video già processati vengono saltati per ID (deduplicazione in-memory
  per singola esecuzione).
- Se i sottotitoli non sono disponibili, il campo resta vuoto.
- I sottotitoli auto-generati sono marcati con `*(auto-generated)*`.
