from bs4 import BeautifulSoup
import requests
import json
import operator


def obtener_urls():
    lista_urls = list()
    with open("titulos_noticias_de_interes", "r") as seguimientos_file:
        contenido = seguimientos_file.readlines()
        for linea in contenido:
            lista_urls.append(linea)
    return lista_urls


def obtener_palabras_url(url):
    page_response = requests.get(url, timeout=5)
    soup = BeautifulSoup(page_response.content, "html.parser")
    textContent = ""
    for node in soup.findAll('p'):
        textContent += str(node.findAll(text=True))
    lista_palabras = textContent.strip(",").strip(".").strip("[").strip("]").strip("(").strip(")").split(" ")
    lista_palabras_lower = [palabra.lower() for palabra in lista_palabras]
    return lista_palabras_lower


def obtener_todas_las_palabras():
    lista_urls = obtener_urls()
    diccionario_palabras = dict()
    for url in lista_urls:
        lista_palabras_url = obtener_palabras_url(url)
        for palabra in lista_palabras_url:
            if palabra not in diccionario_palabras.keys():
                diccionario_palabras[palabra] = 1
            else:
                diccionario_palabras[palabra] += 1
    sorted_x = sorted(diccionario_palabras.items(), key=operator.itemgetter(1))
    top_500_palabras = sorted_x[-500::]
    lista_palabras_dict = list()
    for tupla_palabra in top_500_palabras:
        lista_palabras_dict.append({"palabra":tupla_palabra[0], "peso":
            tupla_palabra[1]})
    with open("palabras_top.json", "w") as palabras_top_file:
        json.dump({"palabras":lista_palabras_dict}, palabras_top_file)

def generar_json_seguimientos():
    with open("titulos_noticias_de_interes", "r") as titulos_de_interes_file:
        pass

def identificar_seguimientos():
    pass

if __name__ == '__main__':
    obtener_todas_las_palabras()
