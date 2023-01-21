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
    color = {
        "ok": 4959823, 
        "wait": 14722834, 
        "warning": 14722834, 
        "no": 13969191, 
        "error": 13969191, 
        "info": 2592725
    }
    # Generator
    def __init__(self, message, username, id, id_channel, timestamp, color, type_) -> None:
        self.embed = {
            "description": f"```\n{message}\n```\n```yml\nname: {username}\nid: {id}\nchannel: {id_channel}\n```",
            "timestamp": timestamp,
            "color": color
        }
        self.type_ = type_

class send():
    def __init__(self, links:dict) -> None:
        self.links = links

    def addqueue(self, webhook:Embed):
        data = eval(open("queue.lst", "r", encoding="utf8").read())
        if webhook.type_ not in data.keys():
            data[webhook.type_] = []
        data[webhook.type_].append(webhook.embed)
        open("queue.lst", "w", encoding="utf8").write(str(data))

    def isSendable(self):
        while True:
            try:
                data = eval(open("queue.lst", "r", encoding="utf8").read())
                return len([1 for key in data.keys() if len(data[key]) > 0]) > 0
            except:
                pass

    def send_webhooks(self):
        data_queue = eval(open("queue.lst", "r", encoding="utf8").read())
        for i in range(3):
            for key in data_queue.keys():
                if len(data_queue[key]) > 0:
                    data = {
                        "content": "",
                        "embeds": data_queue[key],
                        "username": "log",
                        "avatar_url": "https://cdn-icons-png.flaticon.com/512/2965/2965279.png",
                        "attachments": []
                    }
                    result = requests.post(self.links[key][i], json=data, verify=False)
                    if 200 <= result.status_code < 300:
                        print(f"[  OK  ] Webhook sent {result.status_code}")
                        data = eval(open("queue.lst", "r", encoding="utf8").read())
                        for i in data_queue[key]:
                            for elm in data_queue[key]:
                                data[key].remove(elm)
                        open("queue.lst", "w", encoding="utf8").write(str(data))
                        data_queue[key] = []
                    else:
                        print(f"[  NO  ] Not sent with {result.status_code}, response:\n{result.json()}")

class always_run():
    def __init__(self, sender:send) -> None:
        self.work = True
        self.sender = sender

    def __loop__(self):
        while self.work:
            if self.sender.isSendable():
                print("[ WAIT ] Send webhook")
                self.sender.send_webhooks()
            time.sleep(1)

    def run(self):
        Thread(target=self.__loop__).start()

    def stop(self):
        self.work = False
