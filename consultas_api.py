import requests
import flask
import json
import urllib.request
from hackernews import HackerNews

hn = HackerNews()
app = flask.Flask(__name__)

"""URL's de API's"""
hacker_news_url = 'https://hacker-news.firebaseio.com/v0/item/{}'

def cargar_filtros():
    with open("Filtros_FinTech.json", 'r', enconding="utf-8") as filtros_file:
        diccionario_filtros = json.load(filtros_file)
        return diccionario_filtros

@app.route("/")
def index():
   return "Tarea 7"

@app.route("/json")
def retornar_json():
    # /json
    return json.dumps({"arg_1": 1})

@app.route("/Hacker news", methods=["GET"])
def hacker_news():
    """Tomamos el top 100 articulos más populares"""
    palabras = leer_lista_palabras()
    top_stories_ids = hn.top_stories()
    for articulo in top_stories_ids:
        title = hn.item(articulo).title
        url = hn.item(articulo).url

@app.route("/Hacker news", methods=["GET"])
def hacker_news():
    """Tomamos el top 100 articulos más populares"""
    palabras = leer_lista_palabras()
    top_stories_ids = hn.top_stories()
    for articulo in top_stories_ids:
        title = hn.item(articulo).title
        url = hn.item(articulo).url

@app.route("/Twitter", methods=["GET"])
def twitter():
    pass

if __name__ == "__main__":
    hacker_news()