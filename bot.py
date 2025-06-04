
import os
import requests
from flask import Flask, request, jsonify

TOKEN = os.getenv("BOT_TOKEN") or "TON_TOKEN_BOT_ICI"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

@app.route("/resolve-telegram", methods=["POST"])
def resolve_telegram():
    data = request.get_json()
    tg_url = data.get("url", "")

    if "t.me" not in tg_url:
        return jsonify({"error": "URL Telegram invalide"}), 400

    try:
        parts = tg_url.split("/")
        username = parts[3]
        msg_id = parts[4]
        if not msg_id:
            return jsonify({"error": "ID du message manquant"}), 400

        chat_resp = requests.get(f"{API_URL}/getChat?chat_id=@{username}")
        chat_resp.raise_for_status()
        chat_id = chat_resp.json()["result"]["id"]

        msg_resp = requests.get(f"{API_URL}/getChatMessage?chat_id={chat_id}&message_id={msg_id}")
        msg_resp.raise_for_status()
        msg_data = msg_resp.json()["result"]

        file = msg_data.get("document") or msg_data.get("video") or msg_data.get("audio") or msg_data.get("voice")
        if not file and "photo" in msg_data:
            file = msg_data["photo"][-1]

        if not file:
            return jsonify({"error": "Aucun fichier trouvé"}), 404

        file_id = file["file_id"]
        file_info = requests.get(f"{API_URL}/getFile?file_id={file_id}").json()
        file_path = file_info["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        filename = file.get("file_name", "telegram_file")

        return jsonify({ "file_url": file_url, "name": filename })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
