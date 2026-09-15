# YouTube AI Routine

Routine schedulata che cerca video YouTube su un set di keyword configurabili
legate a intelligenza artificiale, estrae i sottotitoli (inglese e italiano)
e salva ogni video come file Markdown individuale.

## Cosa fare quando questa skill viene invocata

1. Assicurarsi che la dipendenza `yt-dlp` sia installata:
   ```
   pip install -r youtube-ai-routine/requirements.txt
   ```
2. Eseguire lo script principale:
   ```
   python3 youtube-ai-routine/routine.py
   ```
3. Lo script:
   - cerca su YouTube i video per ciascuna keyword definita in `KEYWORDS`
     (in cima a `routine.py`);
   - per ogni video trovato, scarica i sottotitoli in inglese (`LANG_PRIMARY`)
     e italiano (`LANG_SECONDARY`), preferendo i sottotitoli umani a quelli
     auto-generati;
   - salva un file `.md` per video nella cartella `output/`, con nome
     `YYYY-MM-DD_titolo-slug.md`, contenente URL, canale, data di
     pubblicazione, durata e le due trascrizioni.
4. Al termine, riportare quanti file `.md` sono stati salvati.

## Note operative

- Lo script richiede accesso di rete in uscita verso `youtube.com` e i
  domini `*.googlevideo.com` (usati per scaricare i sottotitoli). Se la
  policy di rete dell'ambiente blocca questi domini, la routine non può
  completare la ricerca né l'estrazione: verificarlo prima di segnalare un
  bug nello script.
- La configurazione (keyword, numero massimo di risultati per keyword,
  cartella di output, lingue) si modifica direttamente nelle costanti in
  cima a `youtube-ai-routine/routine.py`.
