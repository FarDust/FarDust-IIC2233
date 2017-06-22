import flask
import requests
import re

from flask import request

with open("telegram_token", "r") as file:
    T_TOKEN = file.read().strip()
with open("github_token", "r") as file:
    G_TOKEN = file.read().strip()

URL_TEL_BOT = "https://api.telegram.org/bot{token}".format(**{"token": T_TOKEN})
URL_GIT = "https://api.github.com/repos/FarDust/DrMavrakis4ever/issues/{}"

requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": 413925182, "text": "new_deploy"}).json()
requests.get(URL_TEL_BOT + "/setWebhook", params={"url": "https://drmavrakis4ever.herokuapp.com/telegram",
                                                  "allowed_updates": ["message"]})

app = flask.Flask(__name__)


@app.route("/")
def index():
    return "<h1>I'm a bot</h1>"


@app.route("/admin/<message>")
def admin(message):
    req = requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": 413925182, "text": message})
    return "200 OK"


@app.route("/payload", methods=["POST"])
def github():
    data = request.json
    admin("GitHub say something")
    return "200 OK"


@app.route("/telegram", methods=["POST"])
def telegram():
    data = request.json
    if 'message' in data and 'entities' in data['message']:
        from_data = data['message']['from']
        chat_data = data['message']['chat']
        text = data['message']['text']
        if bool(re.match("\/(get #[0-9]+|post #[0-9]+ \*[\w \n]+|label #[0-9]+ [\w]+|close #[0-9]+)", text)):
            admin("I receive a command")
            if re.match("\/get #[0-9]+", text):
                quarry = text[text.index("#") + 1:].strip()
                get_issue(quarry, chat_data)
            elif re.match("\/close #[0-9]+", text):
                quarry = text[text.index("#") + 1:].strip()
                close_issue(quarry, chat_data)
                pass
            elif re.match("\/label #[0-9]+ [\w]+", text):
                text = text.split(" ")
                label_issue(text[1][1:], text[2], chat_data)
            elif re.match("\/post #[0-9]+ \*[\w \n]+", text):
                text = text.split(" ")
                create_comment(text[1][1:], " ".join(text[2:])[1:], chat_data)
    return "200 OK"


def get_issue(number, chat):
    req = requests.get(url=URL_GIT.format(number), params={"access_token": G_TOKEN})
    if req.status_code == 200:
        message = req.json()['body']
        message = message_format(message, req)
    elif req.status_code == 404:
        message = "Esa issue no existe"
    else:
        message = "Fallo: Error {}".format(req.status_code)
    requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": chat['id'], "text": message})


def close_issue(number, chat):
    req = requests.patch(url=URL_GIT.format(number), params={"access_token": G_TOKEN},
                         data=flask.json.dumps({'state': 'closed'}))
    if req.status_code == 200:
        message = "Issue #{} exitosamente cerrada".format(number)
        message = message_format(message, req)
    elif req.status_code == 404:
        message = "Esa issue no existe"
    else:
        message = "Fallo: Error {}".format(req.status_code)
    requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": chat['id'], "text": message})


def label_issue(number, label, chat):
    labels = requests.get(url=URL_GIT.format(number), params={"access_token": G_TOKEN})
    labels = labels.json()['labels']
    labels.append(label)
    req = requests.patch(url=URL_GIT.format(number), params={"access_token": G_TOKEN},
                         data=flask.json.dumps({'labels': labels}))
    if req.status_code == 200:
        message = "Label '{}' agregada al issue #{}".format(label, number)
        message = message_format(message, req)
    elif req.status_code == 404:
        message = "Esa issue no existe"
    else:
        message = "Fallo: Error {}".format(req.status_code)
    requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": chat['id'], "text": message})


def create_comment(number, message, chat):
    req = requests.patch(url=URL_GIT.format(number)+"/comments", params={"access_token": G_TOKEN},
                         data=flask.json.dumps({"body": message}))
    if req.status_code == 201:
        message = "Se ha comentado en la issue #{}".format(number)
        message = message_format(message, req)
    elif req.status_code == 404:
        print(req.text)
        message = "Esa issue no existe"
    else:
        message = "Fallo: Error {}".format(req.status_code)
    requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": chat['id'], "text": message})


def message_format(message, req):
    formated = req.json()
    formated.update({"message": message})
    formated.update({"user": formated["user"]["login"]})
    template = "[{user}]\n[#{number} - {title}]\n{message}\n[Link: {html_url}]".format(**formated)
    return template

