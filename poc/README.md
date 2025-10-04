# Proof of Concept (PoC) Scripts

Questa directory contiene gli script di dimostrazione per le vulnerabilità identificate nell'analisi di sicurezza di DepthAI.

## Script Disponibili

### `race_condition_poc.py`

**Descrizione:** Dimostra la vulnerabilità di race condition nella funzione `remux_h264_video()` del file `av_writer.py`.

**Utilizzo:**
```bash
python3 race_condition_poc.py
```

**Cosa fa:**
1. Crea un file H.264 di test e un file "vittima" sensibile
2. Avvia un thread "attaccante" che monitora il file H.264
3. Esegue la funzione vulnerabile che elimina e ricrea il file H.264
4. L'attaccante tenta di creare un link simbolico nella finestra temporale vulnerabile
5. Verifica se l'attacco è riuscito controllando se il file vittima è stato sovrascritto

**Output Atteso:**
Lo script mostrerà se l'attacco di race condition è riuscito o fallito. In caso di successo, il contenuto del file vittima sarà stato sovrascritto.

## Note di Sicurezza

⚠️ **IMPORTANTE:** Questi script sono destinati esclusivamente a scopi educativi e di ricerca sulla sicurezza. 

- Non utilizzare questi script su sistemi di produzione
- Non utilizzare per scopi malevoli
- Eseguire solo in ambienti isolati e controllati
- Rispettare sempre le leggi locali e i termini di servizio

## Requisiti

- Python 3.6+
- Sistema operativo Unix-like (Linux/macOS) per il supporto dei link simbolici
- Permessi di scrittura nella directory corrente e in `/tmp/`

## Disclaimer

Gli autori di questi PoC non si assumono alcuna responsabilità per l'uso improprio di questi script. L'obiettivo è migliorare la sicurezza del software attraverso la ricerca responsabile.
