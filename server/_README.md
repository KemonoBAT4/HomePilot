# HomePilot server

Server FastAPI + SQLAlchemy + Postgres, dockerizzato, con:

- CRUD per PC / profili / app dei profili
- discovery automatico dei PC in LAN via mDNS (zeroconf)
- pairing con scambio token (nessun IP o token da inserire a mano)
- invio wake-on-lan

## Avvio

```bash
cp .env.example .env   # personalizza DB_PASSWORD
docker compose up --build
```

L'API risponde su `http://<ip-del-server>:8000`, documentazione automatica su `/docs`.

## Note importanti

- **network_mode: host** è necessario perché il discovery mDNS usa multicast
  UDP, che sulla rete bridge di default di Docker non attraversa il
  container. Funziona su Linux (Raspberry Pi, mini PC, NAS); non è
  pienamente supportato da Docker Desktop su Mac/Windows.
- Il token di pairing viene generato dal server, mandato in chiaro
  all'agente **una sola volta** via LAN, e salvato nel database solo come
  hash (`token_hash`). L'agente lo salva localmente e lo userà per
  autenticare tutte le richieste successive.
- Il modello `ProfileApp` rappresenta una singola applicazione da avviare
  dentro un profilo, con `launch_order` (ordine di avvio) e
  `delay_seconds` (attesa prima del lancio successivo).

## Prossimo passo

L'agente Windows dovrà esporre un piccolo server HTTP locale con almeno:

- `POST /pair` — riceve il token dal server al momento del pairing
- `POST /launch-profile` — riceve la lista di app da avviare (autenticato
  con il token) ed esegue login automatico / avvio app / blocco schermo
