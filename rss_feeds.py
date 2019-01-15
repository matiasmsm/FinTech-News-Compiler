import feedparser
import json

diccionario_noticias = dict()

def cargar_palabras():
    pass
def cargar_fuentes():
    with open("fuentes_rss.json", 'r', encoding="utf-8") as fuentes_file:
        diccionario_fuentes = json.load(fuentes_file)
        return diccionario_fuentes

def consultas_feed():
    diccionario_fuentes = cargar_fuentes()
    for diccionario in diccionario_fuentes["fuentes"]:
        nombre = diccionario["nombre"]
        url = diccionario["url"]
        #peso = diccionario["peso"]
        url_content = feedparser.parse(url)
        titulo = url_content.feed.title
        link = url_content.feed.link
        #subtitulo = url_content.feed.subtitle
        print(titulo, link)
        #filtrar_contenido(url_content)

def filtrar_contenido(content):
    titulo = content.feed.title
    link = content.feed.link
    subtitulo = content.feed.subtitle
    #10 primeras noticias
    for num in range(0, 2):
        titulo_noticia = content.entries[num].title
        descripciom = content.entries[num].description
        link_noticia = content.entries[num].link
        fecha_noticia = content.entries[num].published

def determinar_importancia(titulo, contenido, peso_fuente, autor):
    """Criterios deben ser:
        -Nº de linea donde se menciona la palabra
        -Nº de veces que se menciona la palabra
        -Título y palabras en él
        -Autor
        -Peso de fuente
        -¿Como se toman todos estos criterios en una ecuación?
        -¿Como se clasifican noticias recolectadas en temas automatizadamente?
        """
    pass
consultas_feed()


#peso = diccionario["peso"]
url_content = feedparser.parse(url)
print(nombre, url_content)

