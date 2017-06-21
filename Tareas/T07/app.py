with open("telegram_token", "r") as file:
    T_TOKEN = file.read().strip()
with open("github_token", "r") as file:
    G_TOKEN = file.read().strip()

URL_TEL_BOT = "https://api.telegram.org/bot{token}".format(**{"token": T_TOKEN})
URL_GIT = "https://api.github.com/user"
URL_GOOGLE = "http://www.google.com/search?"
