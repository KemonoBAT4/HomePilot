import sys
import threading

import checkin
import mdns_announce
import pairing_server
from config import load_config, reset_pairing

PAIRING_PORT = 8765


def wait_for_pairing(cfg: dict) -> dict:
    zc, info = mdns_announce.start_announce(cfg["device_id"], PAIRING_PORT)

    paired_event = threading.Event()
    pairing_server.set_on_paired_callback(paired_event.set)

    server_thread = threading.Thread(target=pairing_server.run, args=(PAIRING_PORT,), daemon=True)
    server_thread.start()

    print(f"In attesa di pairing (device_id={cfg['device_id']}, porta {PAIRING_PORT})...")
    paired_event.wait()

    mdns_announce.stop_announce(zc, info)
    return load_config()
# #enddef wait_for_pairing

def main() -> None:
    if ("--reset-pairing" in sys.argv):
        reset_pairing()
        print("Pairing resettato.")
    # #endif

    cfg = load_config()

    if (not cfg["paired"]):
        cfg = wait_for_pairing(cfg)
    # #endif

    print(f"Accoppiato al server {cfg['server_url']}, avvio il polling...")
    checkin.run(cfg["server_url"], cfg["token"])
# #enddef main

if __name__ == "__main__":
    main()
# #endif
