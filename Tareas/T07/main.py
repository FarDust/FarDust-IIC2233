import flask
import requests
import re

from flask import request

from gitbot import analize
from telegram import get_issue, close_issue, label_issue, create_comment, send

with open("telegram_token", "r") as file:
    T_TOKEN = file.read().strip()

URL_TEL_BOT = "https://api.telegram.org/bot{token}".format(**{"token": T_TOKEN})

requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": 413925182, "text": "new_deploy"}).json()
requests.get(URL_TEL_BOT + "/setWebhook", params={"url": "https://drmavrakis4ever.herokuapp.com/telegram",
                                                  "allowed_updates": ["message"]})

app = flask.Flask(__name__)


@app.route("/")
def index():
    return "<h1>I'm a Dr. Mavrakis</h1>"


@app.route("/admin/<message>")
def admin(message):
    requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": 413925182, "text": message})
    return "200 OK"


@app.route("/payload", methods=["POST"])
def github():
    data = request.json
    admin("GitHub webHook")
    analize(data)
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
            elif re.match("\/start", text):
                template = "Hola soy Void un bot creado para controlar el repositorio DrMavrakis4ever.\n" \
                           "Los comandos disponibles te los mostrara telegram al escribir /."
                send(template, chat_data)
    return "200 OK"
