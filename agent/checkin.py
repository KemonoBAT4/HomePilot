import time

import requests

from executor import launch_apps, lock_screen

POLL_INTERVAL_SECONDS = 5


def run(server_url: str, token: str) -> None:
    headers = {"Authorization": f"Bearer {token}"}

    while True:
        try:
            resp = requests.get(f"{server_url}/agent/checkin", headers=headers, timeout=10)
            resp.raise_for_status()
            profile = resp.json().get("profile")
            if profile:
                print(f"[checkin] avvio profilo '{profile['name']}'")
                launch_apps(profile["apps"])
                if profile.get("lock_after_launch"):
                    lock_screen()
        except requests.RequestException as exc:
            print(f"[checkin] server non raggiungibile: {exc}")

        time.sleep(POLL_INTERVAL_SECONDS)
