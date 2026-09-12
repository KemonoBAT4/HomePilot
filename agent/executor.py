import ctypes
import subprocess
import time


def launch_apps(apps: list[dict]) -> None:
    for app in apps:
        command = app["command"]
        args = app.get("args", [])
        try:
            subprocess.Popen([command, *args])
        except OSError as exc:
            print(f"[executor] impossibile avviare {command}: {exc}")

        delay = app.get("delay_seconds", 0)
        if delay:
            time.sleep(delay)


def lock_screen() -> None:
    ctypes.windll.user32.LockWorkStation()
