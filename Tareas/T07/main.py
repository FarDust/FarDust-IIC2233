import flask
import requests

with open("telegram_token", "r") as file:
    T_TOKEN = file.read().strip()

URL_TEL_BOT = "https://api.telegram.org/bot{token}".format(**{"token": T_TOKEN})

requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": 413925182, "text": "new_deploy"}).json()

app = flask.Flask(__name__)


@app.route("/")
def index():
    return "<h1>I'm a bot</h1>"


@app.route("/payload/<load>")
def github(load):
    req = requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": 413925182, "text": load})
    return req.status_code

# app.run(port="")
