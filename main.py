from flask import Flask, request, jsonify
import webhook
import datetime
import os

app = Flask('')
webhook_sender = webhook.send()

@app.route('/')
def home():
	return  "I'm alive"

def savelog(path:str, status:str, message:str, timestamp:datetime):
    path = "log/" + path
    def reformat(t:str):
        if "." in t:
            t += "00000"
            t = ".".join(t.split(".")[:-1]) + "." + t.split(".")[-1][:3]
        else:
            t += ".000"
        return t
    # Check path
    if not os.path.exists(path):
        try:os.makedirs(os.path.dirname(path))
        except:pass
        open(path, "w", encoding="utf8").write("")
    # Save file
    open(path, "a", encoding="utf8").write(f"[{reformat(str(timestamp))}] [{status.upper()}] {message}\n")

@app.route("/log", methods=["POST"])
def logger():
    # Get current time
    current_timestamp = datetime.datetime.now()
    # Check auth
    if "Authorization" not in request.headers.keys() or request.headers["Authorization"] != os.environ["auth_key"]:
        return jsonify({"error": "auth"}), 401
    # Check body
    data = request.json
    if "path" not in data.keys() or "status" not in data.keys() or "message" not in data.keys() or "timestamp" not in data.keys():
        return jsonify({"error": "body"}), 403
    # Convert str to datetime
    data_timestamp = datetime.datetime.strptime(data["timestamp"], "%Y/%m/%d %H:%M:%S.%f")
    # Save log
    savelog(data["path"], data["status"], data["message"], data_timestamp)
    # Send on Discord by webhook
    if "webhook" in data.keys():
        wbhk = data["webhook"]
        webhook_timestamp = data["timestamp"].replace("/", "-").replace(" ", "T") + "Z"
        color = webhook.Embed.color[data["status"]]
        embed = webhook.Embed(data["message"], wbhk["username"],  wbhk["id"], wbhk["channel"], webhook_timestamp, color)
        webhook_sender.addqueue(embed)
    # send.addqueue()
    # Calcul the ping (ms)
    ping = current_timestamp - data_timestamp
    ping = ping.total_seconds()*1000
    # Return status and ping with code 200
    return jsonify({"status": "saved", "ping": str(ping)}), 200

webhook.always_run().run()
app.run(host='0.0.0.0',port=8080)
