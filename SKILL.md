# YouTube AI Routine — Skill

## Cosa fa questa skill

Questa skill esegue la routine automatica di ricerca e trascrizione video
definita in `youtube-ai-routine/routine.py`. La routine:

1. Cerca su YouTube i video corrispondenti alle keyword configurate in
   `KEYWORDS` (in cima al file `routine.py`).
2. Per ogni video trovato, scarica i sottotitoli in inglese (lingua
   primaria) e italiano (lingua secondaria), preferendo i sottotitoli
   caricati manualmente e ricadendo su quelli generati automaticamente
   se necessario.
3. Salva ogni video come file Markdown individuale nella cartella
   `youtube-ai-routine/output/`, con titolo, URL, canale, data di
   pubblicazione, durata e le trascrizioni EN/IT.

## Come eseguirla

```bash
pip install -r youtube-ai-routine/requirements.txt
python3 youtube-ai-routine/routine.py
```

I file `.md` risultanti vengono scritti in `youtube-ai-routine/output/`
(un file per video, nominato `AAAA-MM-GG_titolo-slug.md`).

## Prerequisiti ambientali

- Il pacchetto Python `yt-dlp` deve essere installato (vedi
  `youtube-ai-routine/requirements.txt`). In una sessione remota
  senza hook di setup, va installato manualmente prima di lanciare
  la routine.
- L'ambiente di esecuzione deve poter raggiungere `youtube.com` e i
  domini `*.googlevideo.com` (usati per scaricare i sottotitoli).
  Se la policy di rete della sessione/ambiente blocca questi domini,
  la routine non può completare la ricerca né il download dei
  sottotitoli.

## Configurazione

Tutti i parametri della routine si modificano direttamente in testa a
`youtube-ai-routine/routine.py`:

- `KEYWORDS`: lista di keyword da cercare su YouTube.
- `MAX_RESULTS`: numero massimo di video per keyword.
- `OUTPUT_DIR`: cartella di output dei file Markdown.
- `LANG_PRIMARY` / `LANG_SECONDARY`: lingue dei sottotitoli da estrarre.
