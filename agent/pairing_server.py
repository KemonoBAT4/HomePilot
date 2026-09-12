from flask import Flask, jsonify, request

from config import load_config, save_config

app = Flask(__name__)
_on_paired = None  # callback impostato da main.py


def set_on_paired_callback(callback) -> None:
    global _on_paired
    _on_paired = callback
# #enddef set_on_paired_callback

@app.post("/pair")
def pair():

    cfg = load_config()

    if cfg["paired"]:
        return jsonify({"error": "Gia' accoppiato"}), 409
    # #endif

    data       = request.get_json(silent=True) or {}
    token      = data.get("token")
    server_url = data.get("server_url")

    if not token or not server_url:
        return jsonify({"error": "token e server_url richiesti"}), 400
    # #endif

    cfg["paired"] = True
    cfg["token"] = token
    cfg["server_url"] = server_url
    save_config(cfg)

    if _on_paired:
        _on_paired()
    # #endif

    return jsonify({"status": "paired"})
# #enddef pair

def run(port: int) -> None:
    app.run(host="0.0.0.0", port=port)
# #enddef run