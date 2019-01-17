import feedparser
import json
import datetime

diccionario_noticias = dict()

def cargar_filtros():
    with open("Filtros_FinTech.json", 'r', encoding="utf-8") as filtros_file:
        diccionario_filtros = json.load(filtros_file)
        return diccionario_filtros

def cargar_fuentes():
    with open("fuentes_rss.json", 'r', encoding="utf-8") as fuentes_file:
        diccionario_fuentes = json.load(fuentes_file)
        return diccionario_fuentes

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
    puntaje = 0
    diccionario_filtros = cargar_filtros()
    lista_diccionarios_palabras = diccionario_filtros["palabras"]
    lista_diccionarios_autores = diccionario_filtros["autores"]
    lista_palabras_titulo = titulo.split(" ")
    lista_palabras_contenido = contenido.strip(",").split(" ")
    indice_palabra_titulo = 0
    lista_palabras_fintech_presentes = list()
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
                lista_palabras_fintech_presentes.append(diccionario_palabra[
                                                            "palabra"])
        indice_palabra_titulo += 1
    indice_palabra_contenido = 0
    for palabra_contenido in lista_palabras_contenido:
        #AQUI INCLUIR FACTOR MULTIPLICADOR DE PUNTAJE CON RESPECTO A NUMERO DE
        # LINEA EN QUE SE MENCIONA LA PALABRA
        for diccionario_palabra in lista_diccionarios_palabras:
            dupla_palabras = ""
            if indice_palabra_contenido < len(lista_palabras_contenido)-1:
                dupla_palabras = palabra_contenido+" "+\
                                 lista_palabras_contenido[
                    indice_palabra_contenido+1]
            if palabra_contenido.lower() == diccionario_palabra["palabra"] or \
                            dupla_palabras.lower() == diccionario_palabra[
                        "palabra"]:
                puntaje += diccionario_palabra["peso"]
                lista_palabras_fintech_presentes.append(
                    diccionario_palabra["palabra"])
        indice_palabra_contenido += 1
    """
    for diccionario_autor in lista_diccionarios_autores:
        if diccionario_autor["nombre"] == autor:
            puntaje += diccionario_autor["peso"]
    """
    #Ponderamos un puntaje según conjuntos o subconjuntos de palabras FinTech
    # utilizadas
    puntaje_conjunto_palabras = 0
    for conjunto_palabras in diccionario_filtros["conjuntos_palabras"]:
        resultado = all(elem in lista_palabras_fintech_presentes for elem
                        in conjunto_palabras)
        if resultado:
            print("SI")
            puntaje_conjunto_palabras += 100
    puntaje += puntaje_conjunto_palabras
    return puntaje


def filtrar_contenido(nombre, contenido, peso):
    lista_diccionarios_entries = list()
    for entry in contenido.entries:
        titulo_noticia = entry.title
        resumen = entry.summary
        link_noticia = entry.link
        fecha_actual = datetime.datetime.now().ctime()
        lista_elementos_fecha_actual = fecha_actual.split(" ")
        if "published" in entry.keys():
            lista_elems_fecha_articulo = entry.published.split(" ")
            num_ocurrencias = 0
            for elemento in lista_elementos_fecha_actual:
                for elem in lista_elems_fecha_articulo:
                    if elemento == elem:
                        num_ocurrencias += 1
            if num_ocurrencias == 3:
                puntaje = determinar_importancia(titulo_noticia, resumen, link_noticia,
                                                 peso)
                lista_diccionarios_entries.append({"titulo":titulo_noticia,
                                            "link":link_noticia, "puntaje": puntaje})
                continue
        elif "updated" in entry.keys():
            lista_elems_fecha_articulo = entry.updated.split(" ")
            num_ocurrencias = 0
            for elemento in lista_elementos_fecha_actual:
                for elem in lista_elems_fecha_articulo:
                    if elemento == elem:
                        num_ocurrencias += 1
            if num_ocurrencias == 3:
                puntaje = determinar_importancia(titulo_noticia, resumen,
                                                 link_noticia,
                                                 peso)
                lista_diccionarios_entries.append({"titulo": titulo_noticia,
                                                   "link": link_noticia,
                                                   "puntaje": puntaje})
    return lista_diccionarios_entries


def crear_recopilación_top_noticias(diccionario_fuentes_noticias):
    with open("{}.txt".format(datetime.datetime.now().date()),
              "w") as recopilacion_del_dia_file:
        for fuente in diccionario_fuentes_noticias.keys():
            lista_ordenada_noticias = sorted(diccionario_fuentes_noticias[
                                    fuente], key=lambda k: int(k['puntaje']))
            for noticia in lista_ordenada_noticias:
                if noticia["puntaje"] > 0:
                    recopilacion_del_dia_file.write(noticia["titulo"]+"\n"+
                                                    noticia["link"]+"\n"+"\n")

def consultas_feed():
    diccionario_fuentes = cargar_fuentes()
    diccionario_noticias_fuentes = dict()
    for diccionario in diccionario_fuentes["fuentes"]:
        nombre = diccionario["nombre"]
        url = diccionario["url"]
        peso = diccionario["peso"]
        url_content = feedparser.parse(url)
        lista_entries = filtrar_contenido(nombre, url_content, peso)
        diccionario_noticias_fuentes[nombre] = lista_entries
    crear_recopilación_top_noticias(diccionario_noticias_fuentes)


if __name__ == '__main__':
    consultas_feed()



