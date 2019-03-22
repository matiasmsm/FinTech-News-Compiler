import json
import feedparser

"""with Controller.from_port(port = 9051) as controller:
    controller.authenticate(password='your password set for tor controller port in torrc')
    print("Success!")
    controller.signal(Signal.NEWNYM)
    print("New Tor connection processed")"""



def cargar_fuentes():
    """FUNCIÓN QUE RETORNA EL DICCIONARIO DE LAS FUENTES DE NOTICIAS DE
    fuentes_rss.json"""
    with open("Archivos Json/fuentes_rss.json", 'r', encoding="utf-8") as fuentes_file:
        diccionario_fuentes = json.load(fuentes_file)
        return diccionario_fuentes

def consultas_feed():
    diccionario_fuentes = cargar_fuentes()
    # La variable diccionario_noticias_fuentes es un diccionario en el que cada
    # key es el nombre de una fuente y cada valor respectivo a una key es una
    # lista de noticias que tienen un determinado puntaje (>0 o un top número
    # de noticias)
    diccionario_noticias_fuentes = dict()
    # ------------------------------------------------------------------------
    for diccionario_fuente in diccionario_fuentes["fuentes"]:
        nombre = diccionario_fuente["nombre"]
        print(nombre)
        url = diccionario_fuente["url"]
        peso = diccionario_fuente["peso"]
        url_content = feedparser.parse(url)
        diccionario_noticias_fuentes[nombre] = (nombre, url_content, peso)
    return diccionario_noticias_fuentes
