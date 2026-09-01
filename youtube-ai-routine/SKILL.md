---
name: youtube-ai-routine
description: Cerca su YouTube video recenti legati a intelligenza artificiale (o a qualunque altro insieme di keyword configurabile), scarica i sottotitoli/trascrizioni in inglese e italiano ed esporta ogni video trovato come file Markdown (.md) con titolo, canale, data, URL e trascrizione completa. Usa questa skill ogni volta che l'utente chiede di cercare video YouTube su un argomento e trascriverli, di monitorare periodicamente YouTube per contenuti su AI/LLM/Claude/ChatGPT, o di trasformare i sottotitoli di più video in note Markdown pronte per NotebookLM, Obsidian o altri strumenti di appunti. Fa scattare la skill anche richieste come "trascrivi gli ultimi video su X", "trova video recenti su Claude Code e salvali come markdown", o "esegui la routine YouTube AI".
---

# YouTube AI Routine

Automatizza la ricerca di video YouTube per una lista di keyword, l'estrazione dei
sottotitoli (lingua primaria + secondaria) e il salvataggio di ogni video come
file `.md` autonomo, pronto per essere letto, indicizzato o importato altrove
(es. NotebookLM, Obsidian, un archivio di ricerca).

Lo script che implementa tutta la logica è già pronto in `scripts/routine.py`
(alias di `routine.py` nella cartella della skill): non serve riscriverlo,
basta configurarlo ed eseguirlo.

## Quando usarla

Usa questa skill quando l'utente vuole:
- cercare più video YouTube su uno o più argomenti e ottenerne la trascrizione;
- tenere sotto controllo periodicamente un set di keyword (AI news, LLM, Claude,
  ChatGPT, ecc.) e salvare i nuovi video trovati come note Markdown;
- convertire i sottotitoli di una lista di video in file `.md` con un formato
  coerente (metadati + trascrizione EN + trascrizione IT).

Non serve che l'utente nomini esplicitamente lo script o dica "usa yt-dlp":
basta che chieda di cercare/trascrivere video YouTube per argomento.

## Come procedere

1. **Verifica le dipendenze.** Lo script usa `yt-dlp`. Se non è installato:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configura la ricerca.** Apri `routine.py` e modifica la sezione
   `CONFIGURAZIONE` in cima al file:
   - `KEYWORDS`: lista di stringhe da cercare su YouTube (una ricerca per
     keyword). Sostituisci o estendi la lista di default in base a quello che
     ha chiesto l'utente.
   - `MAX_RESULTS`: quanti video recuperare per ciascuna keyword.
   - `OUTPUT_DIR`: cartella dove salvare i file `.md` (creata automaticamente
     se non esiste).
   - `LANG_PRIMARY` / `LANG_SECONDARY`: codici lingua dei sottotitoli da
     estrarre (es. `"en"`, `"it"`). Lo script prova prima i sottotitoli umani,
     poi quelli auto-generati, e se non trova nulla scrive un placeholder
     ("Sottotitoli non disponibili.") invece di fallire.
3. **Esegui la routine:**
   ```bash
   python routine.py
   ```
   Per ogni keyword, lo script cerca fino a `MAX_RESULTS` video (deduplicando
   quelli già visti tra keyword diverse), estrae i sottotitoli in entrambe le
   lingue e salva un file `.md` per video in `OUTPUT_DIR`, con nome
   `AAAA-MM-GG_titolo-slug.md` (un contatore numerico viene aggiunto in caso
   di collisione).
4. **Riporta all'utente** quanti file sono stati salvati e dove (lo script
   stampa un riepilogo finale), segnalando eventuali video per cui i
   sottotitoli non erano disponibili in una delle due lingue.

## Formato di output

Ogni file Markdown generato segue questa struttura fissa:

```markdown
# <Titolo del video>

- **URL**: <link YouTube>
- **Canale**: <nome canale>
- **Data pubblicazione**: <YYYYMMDD>
- **Durata**: <secondi>
- **Keywords usate**: <keyword che ha trovato questo video>
- **Estratto il**: <data odierna>

---

## Trascrizione (English)

<sottotitoli EN, o "Sottotitoli non disponibili.">

---

## Trascrizione (Italiano)

<sottotitoli IT, o "Non disponibile.">
```

I sottotitoli auto-generati sono preceduti dalla nota `*(auto-generated)*`
così è chiaro quando la trascrizione non è stata rivista da un umano.

## Note operative

- La ricerca usa `ytsearch<N>:<keyword>` di `yt-dlp`, quindi non richiede
  API key di YouTube.
- Lo script mette una pausa di 1 secondo tra un video e l'altro per non
  sovraccaricare YouTube: per liste molto lunghe di keyword/risultati il
  tempo totale di esecuzione può essere significativo, avvisa l'utente se
  la richiesta implica centinaia di video.
- Se una ricerca o l'estrazione sottotitoli di un singolo video fallisce, lo
  script logga l'errore e continua con gli altri video invece di interrompere
  l'intera routine: è normale vedere qualche warning nell'output.
