from requests import request, get, post

URL_TEL_BOT = "https://api.telegram.org/bot423073312:AAE12wJM9zk2LF3NVSLe-LFRwy78kYDX0Js"

print(get(URL_TEL_BOT+"/getMe").json())

