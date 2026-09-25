---
name: youtube-ai-routine
description: >
  Crea o aggiorna una Routine per Claude Code che automatizza: ricerca di
  video su YouTube per keyword configurabili (es. intelligenza artificiale),
  estrazione dei sottotitoli in inglese e italiano, e salvataggio come file
  .md individuali per ogni video. Usa questa skill ogni volta che l'utente
  vuole creare, eseguire o aggiornare uno script per raccogliere, trascrivere
  o archiviare video da YouTube. Attiva anche per: "crea una routine
  YouTube", "voglio scrapare YouTube", "scarica le trascrizioni di video
  YouTube", "automatizza la raccolta di video", "esegui la routine YouTube".
---

# Skill: YouTube AI Routine

Lo script `youtube-ai-routine/routine.py` cerca video su YouTube tramite
keyword configurabili, estrae i sottotitoli esistenti (EN + IT) senza
scaricare l'audio/video, e salva ogni video come file `.md` individuale in
`youtube-ai-routine/output/`.

## IMPORTANTE: limite di rete negli ambienti sandbox

In un ambiente Claude Code on the web / remoto con criteri di rete
restrittivi, l'accesso diretto a `www.youtube.com` puo' essere bloccato dal
proxy dell'ambiente (`CONNECT` rifiutato con 403). Prima di rieseguire da
zero la routine o riscrivere lo script, verifica la raggiungibilita' di
YouTube:

```bash
curl -sS "$HTTPS_PROXY/__agentproxy/status" | grep -A3 recentRelayFailures
curl -sS -o /dev/null -w "HTTP %{http_code}\n" --max-time 20 https://www.youtube.com/
```

Se il proxy risponde 403 su `www.youtube.com`, lo script e' corretto ma non
puo' funzionare in quell'ambiente: il problema e' il criterio di rete
dell'ambiente, non il codice. In questo caso non riscrivere la routine da
zero: segnala il blocco di rete e proponi di eseguire lo script in un
ambiente con accesso a Internet completo (es. locale, o un ambiente con
policy di rete "full access"). Non creare un nuovo branch usa-e-getta con
la stessa documentazione: questo file e' gia' nel branch di lavoro, va solo
aggiornato se cambia qualcosa.

## Passi

1. Verifica se `youtube-ai-routine/routine.py` esiste gia'. Se si', non
   riscriverlo da zero: aggiornalo solo se serve una modifica specifica.
2. Se le keyword non sono configurate o l'utente vuole cambiarle, chiedi:
   > "Quali keyword vuoi usare per la ricerca su YouTube?"
   e aggiorna la costante `KEYWORDS` in cima allo script.
3. Installa le dipendenze: `pip install -r youtube-ai-routine/requirements.txt`.
4. Verifica la raggiungibilita' di YouTube (vedi sopra) prima di eseguire.
5. Esegui: `python3 youtube-ai-routine/routine.py`.
6. Controlla che siano stati creati file `.md` in `youtube-ai-routine/output/`.
   Se lo script fallisce per un errore di rete/proxy, non e' un bug dello
   script: segnalalo com'e'.
7. Mostra il risultato: elenca i file generati e mostra il contenuto di uno
   come esempio.

## Parametri configurabili (in cima a `routine.py`)

| Parametro | Default | Descrizione |
|-----------|---------|-------------|
| `KEYWORDS` | vedi script | Lista di keyword di ricerca |
| `MAX_RESULTS` | `20` | Numero massimo di video per keyword |
| `OUTPUT_DIR` | `"output"` | Cartella di destinazione dei file .md |
| `LANG_PRIMARY` | `"en"` | Lingua principale dei sottotitoli |
| `LANG_SECONDARY` | `"it"` | Lingua secondaria |

## Gestione errori comuni

- **Video senza sottotitoli**: lo script scrive "Sottotitoli non
  disponibili" / "Non disponibile" e continua senza bloccarsi.
- **Sottotitoli solo auto-generati**: usati comunque, con nota
  `*(auto-generated)*`.
