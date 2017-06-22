import flask
import requests
import re
from flask import request

with open("telegram_token", "r") as file:
    T_TOKEN = file.read().strip()

URL_TEL_BOT = "https://api.telegram.org/bot{token}".format(**{"token": T_TOKEN})

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
    if 'entities' in data['message']:
        from_data = data['message']['from']
        chat_data = data['message']['chat']
        text = data['message']['text']
        if bool(re.match("\/(get #[0-9]+|post #[0-9]+ \*[\w \n]+|label #[0-9]+ [\w ]+|close #[0-9]+)", text)):
            admin("I receive a command")
            if re.match("\/get #[0-9]+", text):
                quarry = text[text.index("#"):]
                get_issue(quarry)


    return "200 OK"

def get_issue(number):
    requests.get(URL_TEL_BOT + "/getUpdates").json()

# app.run(port="")
