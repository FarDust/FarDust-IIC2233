import requests
import flask

with open("telegram_token", "r") as file:
    T_TOKEN = file.read().strip()
with open("github_token", "r") as file:
    G_TOKEN = file.read().strip()

URL_TEL_BOT = "https://api.telegram.org/bot{token}".format(**{"token": T_TOKEN})
URL_GIT = "https://api.github.com/user"
URL_GOOGLE = "http://www.google.com/search?"

print(requests.get(URL_TEL_BOT + "/GetUpdates").json())
requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": 413925182, "text": "new_deploy"}).json()
app = flask.Flask(__name__)


@app.route("/")
def index():
    return "<h1>I'm a bot</h1>"


@app.route("/payload/<load>")
def github(load):
    return requests.get(URL_TEL_BOT + "/sendMessage", params={"chat_id": 413925182, "text": load}).json()


if __name__ == '__main__':
    app.run(port=4567)
