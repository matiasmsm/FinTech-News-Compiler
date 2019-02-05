import os
from bs4 import BeautifulSoup
import requests


def recopilar_recopilaciones():
    lista_recopilaciones = list()
    for recopilacion_file in os.listdir("Recopilaciones"):
            lista_urls = obtener_urls("Recopilaciones/{}".format(recopilacion_file))
            lista_recopilaciones.extend(lista_urls)
    return lista_recopilaciones


def obtener_urls(url):
    lista_urls = list()
    with open("{}".format(url), "r", errors='ignore') as recopilacion_file:
        contenido = recopilacion_file.readlines()
        for linea in contenido:
            lista_letras_linea = list(linea)
            if lista_letras_linea[:4] == ["h", "t", "t", "p"]:
                link = ""
                for letra in lista_letras_linea:
                    if letra != "\n":
                        link += letra
                    else:
                        lista_urls.append(link)
    return lista_urls


def obtener_palabras_url(url):
    print(url)
    page_response = requests.get(url, timeout=5)
    soup = BeautifulSoup(page_response.content, "html.parser")
    textContent = ""
    for node in soup.findAll('p'):
        textContent += str(node.findAll(text=True))
    lista_palabras = textContent.strip(",").strip(".").strip("[").strip("]").strip("(").strip(")").split(" ")
    lista_palabras_lower = [palabra.lower() for palabra in lista_palabras]
    return lista_palabras_lower


def obtener_informacion_recopilaciones():
    lista_recopilaciones = recopilar_recopilaciones()
    lista_diccionarios_recopilaciones = list()
    num = len(lista_recopilaciones)
    for url_recopilacion in lista_recopilaciones:
        print(num)
        num -= 1
        lista_palabras = obtener_palabras_url(url_recopilacion)
        lista_diccionarios_recopilaciones.append({"url": url_recopilacion, "lista_palabras": lista_palabras})
    return lista_diccionarios_recopilaciones


def busqueda_noticias(**kwargs):
    for key, value in kwargs.items():
        pass


def busqueda_por_palabras(lista_palabras):
    ranking_noticias_relevantes = list()
    lista_diccionarios_recopilaciones = obtener_informacion_recopilaciones()
    for dict_noticia in lista_diccionarios_recopilaciones:
        puntos = 0
        for palabra_noticia in dict_noticia["lista_palabras"]:
            for palabra_busqueda in lista_palabras:
                if palabra_noticia == palabra_busqueda:
                    puntos += 1
        ranking_noticias_relevantes.append([dict_noticia["url"], puntos])
    ranking_noticias_relevantes = sorted(ranking_noticias_relevantes,
                                            key=lambda k: int(k[1]))
    return ranking_noticias_relevantes


def escribir_html(lista_palabras):
    head_html="""<html>
<head></head>
<body>\n"""
    ranking_noticias = busqueda_por_palabras(lista_palabras)
    print(ranking_noticias)
    for noticia in ranking_noticias:
        head_html += """<p>{}</p>\n""".format(noticia)
    head_html += """</body>\n</html>"""
    with open("resultado.html", "w") as html_file:
        html_file.write(head_html)


if __name__ == '__main__':
    escribir_html(["blockchain"])