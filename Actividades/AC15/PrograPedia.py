import requests

if __name__ == '__main__':
    salir = False
    while not salir:
        respuesta = input("¿Que quieres buscar?: ")
        response = requests.get(url="https://es.wikipedia.org/w/api.php?",
                                params={'action': 'query', 'titles': respuesta, 'prop': 'extracts', 'format': 'json'})
        response = response.json()
        print(list(response['query']['pages'].values())[0]['extract'])
        if respuesta == "salir":
            salir = True
