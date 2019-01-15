import feedparser
import json
import urllib.request
import time
from operator import itemgetter

diccionario_noticias = dict()

def cargar_filtros():
    with open("Filtros_FinTech.json", 'r', encoding="utf-8") as filtros_file:
        diccionario_filtros = json.load(filtros_file)
        return diccionario_filtros

def cargar_fuentes():
    with open("fuentes_rss.json", 'r', encoding="utf-8") as fuentes_file:
        diccionario_fuentes = json.load(fuentes_file)
        return diccionario_fuentes

def consultas_feed():
    diccionario_fuentes = cargar_fuentes()
    diccionario_noticias_fuentes = dict()
    for diccionario in diccionario_fuentes["fuentes"]:
        nombre = diccionario["nombre"]
        url = diccionario["url"]
        peso = diccionario["peso"]
        url_content = feedparser.parse(url)
        #subtitulo = url_content.feed.subtitle
        lista_entries = filtrar_contenido(nombre, url_content, peso)
        diccionario_noticias_fuentes[nombre] = lista_entries
    obtener_top_noticias(diccionario_noticias_fuentes)

def obtener_top_noticias(diccionario_fuentes_noticias):
    nueva_lista_noticias = list()
    for fuente in diccionario_fuentes_noticias.keys():
        lista_ordenada_noticias = sorted(diccionario_fuentes_noticias[fuente], key=lambda k: int(k['puntaje']))
        top_noticias = lista_ordenada_noticias[-3:]
        nueva_lista_noticias.extend(top_noticias)
        nueva_lista_noticias = sorted(nueva_lista_noticias, key=lambda k: int(k['puntaje']))
    print(nueva_lista_noticias)


def filtrar_contenido(nombre, contenido, peso):
    #subtitulo = content.feed.subtitle
    lista_diccionarios_entries = list()
    for entry in contenido.entries:
        llaves_entry = entry.keys()
        #content = urllib.request.urlopen(entry['link']).read()
        #content = entry.content
        titulo_noticia = entry.title
        resumen = entry.summary
        link_noticia = entry.link
        #fecha = entry.published
        #fecha_noticia = content.entries[num].published
        puntaje = determinar_importancia(titulo_noticia, resumen, link_noticia,
                                         peso)
        lista_diccionarios_entries.append({"titulo":titulo_noticia, "puntaje": puntaje})
    return lista_diccionarios_entries


def determinar_importancia(titulo, contenido, link, peso_fuente):
    """Criterios deben ser:
        -N de linea donde se menciona la palabra
        -Nde veces que se menciona la palabra
        -Titulo y palabras en el. LISTO
        -Autor
        -Peso de fuente. LISTO
        -Como se toman todos estos criterios en una ecuacion?. SE SUMAN PUNTOS
        -Como se clasifican noticias recolectadas en temas automatizadamente?
        -CASE INSENSITIVE ****. LISTO
        - Resolver problema de dos palabras juntas. LISTO
        - Más puntaje si existe un conjunto o subconjunto de palabras
        especificas
        """
    puntaje = peso_fuente
    diccionario_filtros = cargar_filtros()
    lista_diccionarios_palabras = diccionario_filtros["palabras"]
    lista_diccionarios_autores = diccionario_filtros["autores"]
    lista_palabras_titulo = titulo.split(" ")
    lista_palabras_contenido = contenido.strip(",").split(" ")
    indice_palabra_titulo = 0
    for palabra_titulo in lista_palabras_titulo:
        for diccionario_palabra in lista_diccionarios_palabras:
            dupla_palabras = ""
            if indice_palabra_titulo < len(lista_palabras_titulo)-1:
                dupla_palabras = palabra_titulo+" "+lista_palabras_titulo[
                    indice_palabra_titulo+1]
            if palabra_titulo.lower() == diccionario_palabra["palabra"] or \
                            dupla_palabras.lower() == diccionario_palabra[
                        "palabra"]:
                puntaje += diccionario_palabra["peso"]
        indice_palabra_titulo += 1
    indice_palabra_contenido = 0
    for palabra_contenido in lista_palabras_contenido:
        #AQUI INCLUIR FACTOR MULTIPLICADOR DE PUNTAJE CON RESPECTO A NUMERO DE
        # LINEA EN QUE SE MENCIONA LA PALABRA
        for diccionario_palabra in lista_diccionarios_palabras:
            dupla_palabras = ""
            if indice_palabra_contenido < len(lista_palabras_contenido)-1:
                dupla_palabras = palabra_contenido+" "+lista_palabras_contenido[
                    indice_palabra_contenido+1]
            if palabra_contenido.lower() == diccionario_palabra["palabra"] or \
                            dupla_palabras.lower() == diccionario_palabra[
                        "palabra"]:
                puntaje += diccionario_palabra["peso"]
        indice_palabra_contenido += 1
    """
    for diccionario_autor in lista_diccionarios_autores:
        if diccionario_autor["nombre"] == autor:
            puntaje += diccionario_autor["peso"]
    """
    return puntaje


consultas_feed()



