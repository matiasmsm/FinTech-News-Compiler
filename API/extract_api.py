import requests
import flask
import json
import urllib.request
from hackernews import HackerNews

hn = HackerNews()
app = flask.Flask(__name__)

"""URL's de API's"""
hacker_news_url = 'https://hacker-news.firebaseio.com/v0/item/{}'

diccionario_fuentes = dict()


def cargar_filtros():
    with open("Archivos Json/Filtros_FinTech.json", 'r', encoding="utf-8") as filtros_file:
        diccionario_filtros = json.load(filtros_file)
        return diccionario_filtros


def obtener_todas_las_noticias():
    hacker_news()
    twitter()
    return diccionario_fuentes

@app.route("/")
def index():
   return "Compiler"


@app.route("/json")
def retornar_json():
    # /json
    return json.dumps({"arg_1": 1})


@app.route("/Hacker news", methods=["GET"])
def hacker_news():
    """Tomamos el top 100 articulos más populares"""
    diccionario_filtros = cargar_filtros()
    palabras = diccionario_filtros["palabras"]
    top_stories_ids = hn.top_stories()
    lista_diccionario_noticias = list()
    for articulo in top_stories_ids:
        title = hn.item(articulo).title
        url = hn.item(articulo).url
        diccionario_noticia = {"titulo": title, "link": url}
        lista_diccionario_noticias.append(diccionario_noticia)
    diccionario_fuentes["Hacker News"] = lista_diccionario_noticias


@app.route("/Twitter", methods=["GET"])
def twitter():
    pass
