import requests
import flask

with open("github_token", "r") as file:
    G_TOKEN = file.read().strip()
with open("telegram_token", "r") as file:
    T_TOKEN = file.read().strip()
URL_TEL_BOT = "https://api.telegram.org/bot{token}".format(**{"token": T_TOKEN})
URL_GIT = "https://api.github.com/repos/FarDust/DrMavrakis4ever/issues/{}"


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
    req = requests.post(url=URL_GIT.format(number) + "/comments", params={"access_token": G_TOKEN},
                        json={"body": message})
    print(req.text)
    if req.status_code == 201:
        message = "Se ha comentado en la issue #{}".format(number)
        getter = requests.get(url=URL_GIT.format(number), params={"access_token": G_TOKEN})
        message = message_format(message, getter)
    elif req.status_code == 404:
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
