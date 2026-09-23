# Routine bloccata dalla policy di rete dell'ambiente

Eseguendo `routine.py` in questo ambiente, ogni richiesta verso
`www.youtube.com` viene rifiutata dal proxy di rete con `403 Forbidden`
("gateway answered 403 to CONNECT (policy denial or upstream failure)").

Questo significa che la routine di scraping YouTube **non può funzionare**
finché la policy di rete dell'ambiente (Claude Code on the web) non
consente l'accesso in uscita a `youtube.com` / `www.youtube.com`.

Per verificarlo di persona:

```bash
curl -sS "$HTTPS_PROXY/__agentproxy/status"
```

e controllare `recentRelayFailures` per voci con `host: "www.youtube.com:443"`.

## Cosa serve per sbloccarla

Cambiare la network policy dell'ambiente/sessione in modo da consentire
l'uscita verso YouTube (es. policy "allow all" o un allowlist che includa
`youtube.com`). Vedi la documentazione di Claude Code on the web per le
opzioni di configurazione della rete.

## Nota sui branch

Diverse esecuzioni precedenti di questa routine automatica hanno creato
molti branch `claude/trusting-dijkstra-*` (30+), tutti derivati dallo
stesso commit base `88a6ab1` e mai uniti tramite pull request: nessuno
contiene output reale (solo `output/.gitkeep`), perché nessuna esecuzione
è mai riuscita a raggiungere YouTube. Vale la pena valutare una pulizia
di quei branch una volta risolta la policy di rete.
