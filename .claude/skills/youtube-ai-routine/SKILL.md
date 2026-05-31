---
name: youtube-ai-routine
description: >
  Crea una Routine completa per Claude Code che automatizza: scraping di YouTube
  per video sull'IA (o qualsiasi keyword configurabile), estrazione dei sottotitoli
  in inglese e italiano, e salvataggio come file .md individuali per ogni video.
  Usa questa skill ogni volta che l'utente vuole creare uno script o una routine
  automatizzata per raccogliere, trascrivere o archiviare video da YouTube,
  specialmente su temi come intelligenza artificiale, AI news, ricerca,
  o qualsiasi altro argomento configurabile. Attiva anche per: "crea una routine
  YouTube", "voglio scrapare YouTube", "scarica le trascrizioni di video YouTube",
  "automatizza la raccolta di video", "crea uno script per YouTube", "routine
  per trascrivere video".
---

# Skill: YouTube AI Routine

Questa skill guida Claude Code nella creazione di una **Routine Python completa**
che:

1. Cerca video su YouTube tramite keyword configurabili
2. Estrae i sottotitoli esistenti (EN + IT) senza scaricare l'audio
3. Salva ogni video come file `.md` individuale con metadati e testo

---

## Panoramica della Routine da creare

La routine è composta da **un singolo script Python** (`routine.py`) con
dipendenze minime. Non richiede API key YouTube (usa `yt-dlp` + `youtube-search-python`).

### Struttura dell'output

```
output/
├── 2025-05-13_video-title-slug.md
├── 2025-05-13_altro-video.md
└── ...
```

### Formato di ogni file `.md`

```markdown
# Titolo del Video

- **URL**: https://youtube.com/watch?v=XXXX
- **Canale**: Nome Canale
- **Data pubblicazione**: 2025-05-13
- **Durata**: 12:34
- **Keywords usate**: artificial intelligence, AI news

---

## Trascrizione (English)

[testo sottotitoli in inglese...]

---

## Trascrizione (Italiano)

[testo sottotitoli in italiano, o "Non disponibile" se assente]
```

---

## Istruzioni per Claude Code

Quando questa skill viene attivata, segui questi passi nell'ordine:

### Step 1 — Chiedi le keyword all'utente

Prima di scrivere qualsiasi codice, chiedi:

> "Quali keyword vuoi usare per la ricerca su YouTube?
> Esempio: `artificial intelligence, AI news, large language models`"

Salva le keyword come lista configurabile nello script.

### Step 2 — Installa le dipendenze

```bash
pip install yt-dlp youtube-search-python
```

Verifica che l'installazione vada a buon fine prima di procedere.

### Step 3 — Crea lo script `routine.py`

Usa il template qui sotto come base. Sostituisci `KEYWORDS` con quelle
fornite dall'utente.

Leggi il file di riferimento per il codice completo:
→ `references/routine_template.md`

### Step 4 — Crea la cartella di output

```bash
mkdir -p output
```

### Step 5 — Esegui e verifica

```bash
python routine.py
```

Controlla che almeno 3–5 file `.md` siano stati creati nella cartella `output/`.
Se ci sono errori, diagnosticali e correggi lo script prima di consegnarlo.

### Step 6 — Mostra il risultato all'utente

Elenca i file `.md` generati e mostra il contenuto di uno come esempio.

---

## Parametri configurabili (da esporre all'utente)

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `KEYWORDS` | `["artificial intelligence"]` | Lista di keyword di ricerca |
| `MAX_RESULTS` | `20` | Numero massimo di video per keyword |
| `OUTPUT_DIR` | `"output"` | Cartella di destinazione dei file .md |
| `LANG_PRIMARY` | `"en"` | Lingua principale dei sottotitoli |
| `LANG_SECONDARY` | `"it"` | Lingua secondaria (fallback: auto-generati) |

---

## Gestione errori comuni

- **Video senza sottotitoli**: scrivi `"Sottotitoli non disponibili"` nel campo
  trascrizione e continua senza bloccarti.
- **Sottotitoli solo auto-generati**: usali comunque, aggiungi nota
  `*(auto-generated)*` nel file .md.
- **Rate limiting YouTube**: aggiungi `time.sleep(1)` tra una richiesta e l'altra.
- **Titoli con caratteri speciali**: sanitizza il titolo per il nome file
  (rimuovi `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`).

---

## Note tecniche

- `yt-dlp` è preferito a `pytube` perché più aggiornato e affidabile.
- I sottotitoli vengono scaricati come `.vtt`, poi convertiti in testo pulito
  (rimuovendo i tag temporali).
- Se i sottotitoli italiani non esistono come traduzione umana, prova con
  il codice `it` degli auto-caption. Se neanche quelli esistono, scrivi
  `"Non disponibile"`.
- La routine è pensata per essere eseguita periodicamente (es. con `cron`
  o Task Scheduler di Windows).
