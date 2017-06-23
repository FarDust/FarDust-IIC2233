import re

import requests

with open("github_token", "r") as file:
    G_TOKEN = file.read().strip()
with open("telegram_token", "r") as file:
    T_TOKEN = file.read().strip()
with open("google_token", "r") as file:
    GOO_TOKEN = file.read().strip()
with open("google_cx", "r") as file:
    GOO_CX = file.read().strip()

URL_TEL_BOT = "https://api.telegram.org/bot{token}".format(**{"token": T_TOKEN})
URL_GIT = "https://api.github.com/repos/FarDust/DrMavrakis4ever/issues/{}"
URL_GOO = "https://www.googleapis.com/customsearch/v1"


def analize(response: dict):
    if "action" in response and response["action"] == 'opened' or True:
        print(response['issue'].keys())
        if "body" in response['issue']:
            if re.match("(Traceback)[^\n]+\n[^\n]+\n[^\n]+\n[^\n]+$", response['issue']["body"]):
                sender_q = re.search("(Traceback).+\n.+\n.+\n.+", response['issue']["body"]).group()
                google_response = requests.get(URL_GOO,params={"q":sender_q, "key": GOO_TOKEN, "cx": GOO_CX})
                print(google_response.json())
                return "200 OK"
            else:
                return "dude"
        else:
            return "nobody"

