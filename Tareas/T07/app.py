import requests
from flask import json

with open("telegram_token", "r") as file:
    T_TOKEN = file.read().strip()
with open("github_token", "r") as file:
    G_TOKEN = file.read().strip()

URL_TEL_BOT = "https://api.telegram.org/bot{token}".format(**{"token": T_TOKEN})
URL_GIT = "https://api.github.com/repos/FarDust/DrMavrakis4ever/issues/2"
URL_GOOGLE = "http://www.google.com/search?"

print(requests.patch(url=URL_GIT,params={"access_token": G_TOKEN}, data=json.dumps({'labels': ["bug"]})).text)
