import time
import requests

from executor import launch_apps, lock_screen

POLL_INTERVAL_SECONDS: int = 10

def run(server_url: str, token: str) -> None:
    """
    #### DESCRIPTION:
    Runs the checkin loop

    #### PARAMETERS:
    - `server_url` (`str`): The URL of the server
    - `token` (`str`): The token of the PC

    #### RETURNS:
    No return
    """

    headers: dict[str, str] = {"Authorization": f"Bearer {token}"}

    while True:
        try:
            resp = requests.get(f"{server_url}/agent/checkin", headers=headers, timeout=10)
            resp.raise_for_status()
            profile = resp.json().get("profile")
            if (profile is not None):
                print(f"[checkin] avvio profilo '{profile['name']}'")
                launch_apps(profile["apps"])
                if profile.get("lock_after_launch"):
                    lock_screen()
                # #endif
            # #endif
        except requests.RequestException as exc:
            print(f"[checkin] server non raggiungibile: {exc}")
        # #endtry

        time.sleep(POLL_INTERVAL_SECONDS)
    # #endwhile
# #enddef run
