import os
import time
import requests
from threading import Thread

class Embed():
    # Color
    ok=4959823
    wait=14722834
    warning=14722834
    no=13969191
    error=13969191
    info=2592725
    # Generator
    def __init__(self, message, username, id, id_channel, timestamp, color) -> None:
        self.embed = {
            "description": f"```\n{message}\n```\n```yml\nname: {username}\nid: {id}\nchannel: {id_channel}\n```",
            "timestamp": timestamp,
            "color": color
        }

class send():
    def addqueue(webhook):
        data = eval(open("queue.lst", "r", encoding="utf8").read())
        data.append(webhook.embed)
        open("queue.lst", "w", encoding="utf8").write(str(data))

    def isSendable():
        return len(eval(open("queue.lst", "r", encoding="utf8").read())) > 0

    def send_webhooks(url):
        data = eval(open("queue.lst", "r", encoding="utf8").read())
        data = {
            "content": "",
            "embeds": data,
            "username": "log",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/2965/2965279.png",
            "attachments": []
        }
        result = requests.post(url, json=data)
        if 200 <= result.status_code < 300:
            print(f"[  OK  ] Webhook sent {result.status_code}")
        else:
            print(f"[  NO  ] Not sent with {result.status_code}, response:\n{result.json()}")

class always_run():
    def __init__(self) -> None:
        self.index = 0
        self.webhook = [
            os.environ["webhoob_1"], 
            os.environ["webhoob_2"], 
            os.environ["webhoob_3"]
        ]

    def __index_update__(self):
        self.index += 1
        if self.index > len(self.webhook):
            self.index = 0

    def __loop__(self):
        if send.isSendable():
            send.send_webhooks(self.webhook[self.index])
            self.__index_update__()
        time.sleep(1)

    def run(self):
        Thread(target=self.__loop__).start()