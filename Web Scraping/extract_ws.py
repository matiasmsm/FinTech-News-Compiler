from bs4 import BeautifulSoup
import requests
import json


def cargar_filtros():
    with open("Filtros_FinTech.json", 'r', encoding="utf-8") as filtros_file:
        diccionario_filtros = json.load(filtros_file)
        return diccionario_filtros

def cargar_fuentes():
    with open("fuentes_web_scraping.json", 'r', encoding="utf-8") as fuentes_file:
        diccionario_fuentes = json.load(fuentes_file)
        return diccionario_fuentes

def obtener_palabras_url(url):
    page_response = requests.get(url, timeout=5)
    soup = BeautifulSoup(page_response.content, "html.parser")
    textContent = ""
    for node in soup.findAll('p'):
        textContent += str(node.findAll(text=True))
    lista_palabras = textContent.strip(",").strip(".").strip("[").strip(
        "]").strip("(").strip(")").split(" ")
    lista_palabras_lower = [palabra.lower() for palabra in lista_palabras]
    return lista_palabras_lower

