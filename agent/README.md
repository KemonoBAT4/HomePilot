# HomePilot agent (Windows)

Nessun autologin: l'agente parte quando fai il login manuale, chiede al
server se c'e' un profilo in attesa (richiesto da te via mobile) e lo
esegue. Se non c'e' nulla in attesa, resta semplicemente in ascolto.

## Primo avvio (pairing)

```bash
pip install -r requirements.txt
python main.py
```

L'agente si annuncia in LAN via mDNS e resta in attesa. Dall'app mobile
(o per ora da `/docs` sul server) approvi il pairing — a quel punto
l'agente riceve token e indirizzo del server, li salva in
`~/.homepilot/config.json`, e passa al loop di polling.

Per resettare il pairing (es. hai cambiato server):
```bash
python main.py --reset-pairing
```

## Avvio automatico al login

Registralo con il Task Scheduler di Windows, trigger "al logon" — **non**
come servizio: deve girare nella sessione interattiva per poter aprire
finestre visibili.

```powershell
$action  = New-ScheduledTaskAction -Execute "pythonw.exe" -Argument "C:\percorso\homepilot-agent\main.py"
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "HomePilotAgent" -Action $action -Trigger $trigger -RunLevel Limited
```

`pythonw.exe` invece di `python.exe` evita la finestra di console.

## Note

- Il polling verso `/agent/checkin` avviene ogni 5 secondi (`checkin.py`),
  sia appena dopo il login (profilo in attesa da quando eri fuori) sia
  mentre il PC e' gia' acceso e loggato (comando "live" da mobile).
- L'agente non avvia mai nulla di sua iniziativa: l'unica cosa che puo'
  far scattare un profilo e' una richiesta esplicita fatta dal mobile,
  che il server mette in coda (`pending_profile_id`) finche' l'agente
  non la ritira al polling successivo.
- Per ora solo Windows (`executor.py` usa `ctypes.windll`); l'adapter
  Linux arriva quando si passa al PC Ubuntu/Debian.
