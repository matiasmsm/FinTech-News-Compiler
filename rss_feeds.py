import feedparser
import json

diccionario_noticias = dict()

def cargar_filtros():
    with open("Filtros_FinTech.json", 'r', enconding="utf-8") as filtros_file:
        diccionario_filtros = json.load(filtros_file)
        return diccionario_filtros
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
        -N de linea donde se menciona la palabra
        -Nde veces que se menciona la palabra
        -Titulo y palabras en el
        -Autor
        -Peso de fuente
        -Como se toman todos estos criterios en una ecuacion?
        -Como se clasifican noticias recolectadas en temas automatizadamente?
        -CASE INSENSITIVE ****
        - Resolver problema de dos palabras juntas
        """
    puntaje = peso_fuente
    diccionario_filtros = cargar_filtros()
    lista_diccionarios_palabras = diccionario_filtros["palabras"]
    lista_diccionarios_autores = diccionario_filtros["autores"]
    lista_palabras_titulo = titulo.split(" ")
    lista_palabras_contenido = contenido.split(" ")
    for palabra_titulo in lista_palabras_titulo:
        for diccionario_palabra in lista_diccionarios_palabras:
            if palabra_titulo == diccionario_palabra["palabra"]:
                puntaje += diccionario_palabra["peso"]
    for palabra_contenido in lista_palabras_contenido:
        #AQUI INCLUIR FACTOR MULTIPLICADOR DE PUNTAJE CON RESPECTO A NUMERO DE LINEA EN QUE SE MENCIONA LA PALABRA
        for diccionario_palabra in lista_diccionarios_palabras:
            if palabra_contenido == diccionario_palabra["palabra"]:
                puntaje += diccionario_palabra["peso"]
    for diccionario_autor in lista_diccionarios_autores:
        if diccionario_autor["nombre"] == autor:
            puntaje += diccionario_autor["peso"]
    return puntaje



consultas_feed()


#peso = diccionario["peso"]
url_content = feedparser.parse(url)
print(nombre, url_content)

