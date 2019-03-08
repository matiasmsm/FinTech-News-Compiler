import datetime
import json
import re

from RSS.extract_rss import consultas_feed


def cargar_filtros():
    """FUNCIÓN QUE RETORNA EL DICCIONARIO DE FILTROS DE Filtros_FinTech.json"""
    with open("Archivos Json/Filtros_FinTech.json", 'r', encoding="utf-8") as filtros_file:
        diccionario_filtros = json.load(filtros_file)
        return diccionario_filtros


def cargar_combinaciones_palabras():
    with open("Archivos Json/combinaciones_palabras.json", "r") as combinaciones_file:
        lista_combinaciones = json.load(combinaciones_file)["combinaciones"]
        return lista_combinaciones


def determinar_estadisticas(palabras_fintech, lista_dict_palabras):
    """Función que determina y retorna estadisticas del % de mención de palabras
    FinTech presentes en la noticias"""
    lista_estadisticas_palabras = list()
    lista_palabras_ya_incluidas = list()
    for palabra in palabras_fintech:
        if palabra not in lista_palabras_ya_incluidas:
            lista_palabras_ya_incluidas.append(palabra)
            numero_menciones = 0
            for palabra2 in palabras_fintech:
                if palabra == palabra2:
                    numero_menciones += 1
            porcentaje_mencion = (numero_menciones/len(palabras_fintech))*100
            lista_estadisticas_palabras.append([palabra, porcentaje_mencion])
    str_estadisticas = ""
    indice_lista_estadisticas = 0
    for lista in lista_estadisticas_palabras:
        if indice_lista_estadisticas == len(lista_estadisticas_palabras)-1:
            str_estadisticas += str(str(lista[0]) + ": "+"{0:.2f}".format(lista[1])+"%")
        else:
            str_estadisticas += str(str(lista[0])+": "+"{0:.2f}".format(lista[1])+"%"", ")
        indice_lista_estadisticas += 1
    return str_estadisticas


def determinar_tema(palabras_fintech_titulo, palabras_fintech_contenido):
    """Función que determina y retorna el tema(eje) de una noticia"""
    lista_palabras_fintech = cargar_filtros()["palabras"]
    ejes_en_titulo = list()
    for palabra_titulo in palabras_fintech_titulo:
        for dict_palabra in lista_palabras_fintech:
            if "eje" in dict_palabra.keys() and dict_palabra["palabra"] == palabra_titulo:
                ejes_en_titulo.append(dict_palabra["eje"])
    ejes_en_contenido = list()
    for palabra_contenido in palabras_fintech_contenido:
        for dict_palabra in lista_palabras_fintech:
            if "eje" in dict_palabra.keys() and dict_palabra["palabra"] == palabra_contenido:
                ejes_en_contenido.append(dict_palabra["eje"])
    if len(ejes_en_titulo) > 0:
        lista_ejes_titulo_estadistica = list()
        lista_ejes_mencionados = list()
        for eje in ejes_en_titulo:
            if eje not in lista_ejes_mencionados:
                lista_ejes_mencionados.append(eje)
                numero_de_mencion = 0
                for eje2 in ejes_en_titulo:
                    if eje == eje2:
                        numero_de_mencion += 1
                lista_ejes_titulo_estadistica.append([eje, numero_de_mencion])
        lista_ejes_titulo_estadistica = sorted(lista_ejes_titulo_estadistica, key=lambda k: int(k[1]))
        """CASOS EN QUE HAY 2 EJES CON EL MISMO NUMERO DE MENCIÓN"""
        num_men_top_ej = lista_ejes_titulo_estadistica[-1][1]
        if len(lista_ejes_titulo_estadistica) >=2 :
            if lista_ejes_titulo_estadistica[len(lista_ejes_titulo_estadistica)-2][1] == num_men_top_ej:
                top_2 = lista_ejes_titulo_estadistica[-2:]
                if top_2[1][0] == "Otro":
                    eje = top_2[0][0]
                    print(eje, ejes_en_titulo, ejes_en_contenido)
                    return eje
                else:
                    print(top_2[1][0], ejes_en_titulo, ejes_en_contenido)
                    return top_2[1][0]
            else:
                eje = lista_ejes_titulo_estadistica[-1][0]
                print(eje, ejes_en_titulo, ejes_en_contenido)
                return eje
        else:
            eje = lista_ejes_titulo_estadistica[-1][0]
            print(eje, ejes_en_titulo, ejes_en_contenido)
            return eje
    elif len(ejes_en_contenido) > 0:
        lista_ejes_contenido_estadistica = list()
        lista_ejes_mencionados = list()
        for eje in ejes_en_contenido:
            if eje not in lista_ejes_mencionados:
                lista_ejes_mencionados.append(eje)
                numero_de_mencion = 0
                for eje2 in ejes_en_contenido:
                    if eje == eje2:
                        numero_de_mencion += 1
                lista_ejes_contenido_estadistica.append([eje, numero_de_mencion])
        lista_ejes_contenido_estadistica = sorted(lista_ejes_contenido_estadistica,
                                               key=lambda k: int(k[1]))
        num_men_top_ej = lista_ejes_contenido_estadistica[-1][1]
        if len(lista_ejes_contenido_estadistica) >= 2:
            if lista_ejes_contenido_estadistica[len(
                    lista_ejes_contenido_estadistica) - 2][1] == \
                    num_men_top_ej:
                top_2 = lista_ejes_contenido_estadistica[-2:]
                if top_2[1][0] == "Otro":
                    eje = top_2[0][0]
                    print(eje, ejes_en_titulo, ejes_en_contenido)
                    return eje
                else:
                    print(top_2[1][0], ejes_en_titulo, ejes_en_contenido)
                    return top_2[1][0]
            else:
                eje = lista_ejes_contenido_estadistica[-1][0]
                print(eje, ejes_en_titulo, ejes_en_contenido)
                return eje
        else:
            eje = lista_ejes_contenido_estadistica[-1][0]
            print(eje, ejes_en_titulo, ejes_en_contenido)
            return eje
    else:
        print("Otro", ejes_en_titulo, ejes_en_contenido)
        return "Otro"

"""
def filtro_data_top_noticias(lista_palabras_contenido):
    with open("palabras_top.json", "r") as palabras_top_file:
        diccionario_json = json.load(palabras_top_file)
    lista_dict_palabras = diccionario_json["palabras"]
    peso = 0
    for palabra_contenido in lista_palabras_contenido:
        for dict_palabra in lista_dict_palabras:
            palabra, numero_menciones = dict_palabra.values()
            if palabra_contenido == palabra:
                peso += numero_menciones
    return peso
"""

def tiene_eje(palabra, lista_dict_palabras):
    """Función que retorna True si la palabra FinTech tiene un eje asignado y
    si no retorna False"""
    for dict_palabra in lista_dict_palabras:
        if dict_palabra["palabra"] == palabra:
            if "eje" in dict_palabra.keys():
                return True
            else:
                return False


def determinar_importancia(titulo, contenido, link, peso_fuente):
    """
    FUNCIÓN QUE A PARTIR DE DISTINTOS FILTROS DETERMINA EL PUNTAJE DE UNA
    NOTICIA

    Criterios deben ser:
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
    #url_entry_parsed = feedparser.parse(link)
    # Se definen en variables las listas de filtros
    diccionario_filtros = cargar_filtros()
    lista_diccionarios_palabras = diccionario_filtros["palabras"]
    lista_diccionarios_autores = diccionario_filtros["autores"]
    lista_palabras_no_deseadas = diccionario_filtros["palabras no queridas"]
    #lista_listas_conjuntos_palabras = diccionario_filtros["conjuntos_palabras"]
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Se separan las palabras del titulo y del contenido y se ponen en sus
    # listas respectivas
    regex = r'\b\w+\b'
    lista_palabras_titulo = re.findall(regex, titulo)
    lista_palabras_contenido = re.findall(regex, contenido)
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Lista a la que se le agregan las palabras FinTech presentes en el
    # articulo
    lista_palabras_fintech_presentes = list()
    lista_indices_palabras_fintech_presentes = list()
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    """SE DESCARTA
    NOTICIA SI CONTIENE PALABRAS NO DESEADAS EN EL TÍTULO"""
    for palabra_titulo in lista_palabras_titulo:
        for palabra_no_deseada in lista_palabras_no_deseadas:
            if palabra_titulo.lower() == palabra_no_deseada.lower():
                return 0, [], "Otro", "{}"
    """PRIMER FILTRO: DE PRESENCIA DE PALABRAS FINTECH EN TITULO
    SE DEBE DAR UN PUNTAJE BASE A LA NOTICIA BAJO ESTE CRITERIO. """
    indice_palabra_titulo = 0
    for palabra_titulo in lista_palabras_titulo:
        for diccionario_palabra in lista_diccionarios_palabras:
            # variable dupla_palabras es para palabras FinTech que se componen
            # de 2 palabras (por ejemplo: "banco central")
            dupla_palabras = ""
            # indice de segunda palabra que compone dupla_palabra no debe ser
            # superior al largo de lista_palabras_titulo
            if indice_palabra_titulo < len(lista_palabras_titulo)-1:
                dupla_palabras = palabra_titulo+" "+lista_palabras_titulo[
                    indice_palabra_titulo+1]
            # se ocupa .lower() para que sea case-insensitive
            if palabra_titulo.lower() == diccionario_palabra["palabra"] or \
                            dupla_palabras.lower() == diccionario_palabra[
                        "palabra"]:
                """**** SE DEBE VER BIEN QUE PUNTAJE DAR ****"""
                puntaje += diccionario_palabra["peso"]*10
                """**** AQUI VER SI HACER UNA LISTA DE PALABRAS SOLO PARA
                TITULO O DEJARLA COMO ESTÁ, QUE ES EN CONJUNTO CON PALABRAS
                DEL ARTICULO ****"""
                lista_palabras_fintech_presentes.append(diccionario_palabra[
                                                            "palabra"])
        indice_palabra_titulo += 1

    """Añadimos a lista_palabras_fintech_presentes las palabras FinTech que
    están presentes en el contenido de la noticia"""
    indice_palabra_contenido = 0
    for palabra_contenido in lista_palabras_contenido:
        for diccionario_palabra in lista_diccionarios_palabras:
            dupla_palabras = ""
            if indice_palabra_contenido < len(lista_palabras_contenido)-1:
                dupla_palabras = palabra_contenido+" "+\
                                 lista_palabras_contenido[
                    indice_palabra_contenido+1]
            if palabra_contenido.lower() == diccionario_palabra["palabra"] or \
                            dupla_palabras.lower() == diccionario_palabra[
                        "palabra"]:
                lista_palabras_fintech_presentes.append(
                    diccionario_palabra["palabra"])
                lista_indices_palabras_fintech_presentes.append(
                    indice_palabra_contenido)
        indice_palabra_contenido += 1


    """SEGUNDO FILTRO: SE LE SUMA UN PUNTAJE ELEVADO A LA NOTICIA SI ES QUE
    MENCIONA CONJUNTOS DE PALABRAS ESPECIFICAS DEFINIDAS EN LA LISTA
    lista_palabras_contenido"""
    # La variable puntaje_conjunto_palabras representa la suma total de
    # puntajes por mención de conjuntos de palabras en el articulo
    puntaje_conjunto_palabras = 0
    lista_combinaciones = cargar_combinaciones_palabras()
    lista_conjunto_palabras_mencionadas = list()
    for conjunto_palabras in lista_combinaciones:
        # En la siguiente linea se revisa si el el conjunto_palabras está en
        # la lista lista_palabras_fintech_presentes
        existe_eje = False
        for elem in conjunto_palabras:
            if tiene_eje(elem, lista_diccionarios_palabras):
                resultado = all(elem in lista_palabras_fintech_presentes for elem
                                in conjunto_palabras)
                if resultado:
                    # Aqui se le suma un puntaje (**** POR DETERMINAR ****) si el
                    # conjunto_palabras está presente en la lista
                    # lista_palabras_fintech_presentes
                    puntaje_conjunto_palabras += 200
                    lista_conjunto_palabras_mencionadas.append(conjunto_palabras)
    puntaje += puntaje_conjunto_palabras
    """FILTRO POR AUTORES (FALTA DEFINIR AUTORES)"""
    """autor
    for diccionario_autor in lista_diccionarios_autores:
        if diccionario_autor["nombre"] == autor:
            puntaje = puntaje*diccionario_autor["peso"]"""

    """FILTRO POR REPUTACIÓN DE FUENTE"""
    puntaje = puntaje*peso_fuente
    str_estadisticas = determinar_estadisticas(lista_palabras_fintech_presentes, lista_diccionarios_palabras)
    tema_global_noticia = determinar_tema(lista_palabras_titulo, lista_palabras_fintech_presentes)
    return puntaje, lista_conjunto_palabras_mencionadas, tema_global_noticia, str_estadisticas


def filtrar_contenido(nombre_fuente, contenido, peso):
    """AQUI SE RETORNA UNA LISTA CON DICCIONARIOS QUE REPRESENTAN Y TIENE
    LOS DETALLES RELEVANTES DE UN ARTICULO DE LA FUENTE ESPECIFICADA"""
    # La variable lista_diccionario_entries es una lista de diccionarios en la
    # cual cada diccionario representa una noticia del día de hoy con las
    # llaves "titulo", "link" y "puntaje"
    lista_diccionarios_entries = list()
    # ------------------------------------------------------------------------
    for entry in contenido.entries:
        """Loop por todos los articulos de la fuente"""
        titulo_noticia = entry.title
        """AQUI EL PROBLEMA"""
        contenido = entry.summary
        """----------------------"""
        link_noticia = entry.link
        fecha_actual = datetime.datetime.now().ctime()
        # Se separa el string de la fecha en sus componentes para asi poder
        # obtener las noticias que han salido sólo el día de hoy
        lista_elementos_fecha_actual = fecha_actual.split(" ")
        """La llave 'published' no siempre existe en el diccionario entregado por
         el RSS feed por lo que se debe tomar en cuenta la llave 'updated'"""
        if "published" in entry.keys():
            if "-" in entry.published:
                lista1_elems_fecha_articulo = entry.published.split("T")
                lista_elems_fecha_articulo = list()
                for elem in lista1_elems_fecha_articulo:
                    lista_elems_fecha_articulo.extend(elem.split("-"))
            else:
                lista_elems_fecha_articulo = entry.published.split(" ")
            num_ocurrencias = 0
            for elemento in lista_elementos_fecha_actual:
                if len(elemento) == 1:
                    elemento = '0' + elemento
                for elem in lista_elems_fecha_articulo:
                    if elemento == elem:
                        num_ocurrencias += 1
            if num_ocurrencias == 3:
                """Si es que la fecha de publicación de la noticia es el día de
                 hoy entonces determinar el puntaje de la noticia"""
                puntaje, lista_conjunto_palabras, tema, estadisticas = \
                    determinar_importancia(titulo_noticia, contenido,
                                           link_noticia,
                                                 peso)
                lista_diccionarios_entries.append({"titulo":titulo_noticia,
                                            "link":link_noticia, "puntaje":
                                            puntaje, "conjunto_palabras":
                                            lista_conjunto_palabras,
                                            "tema": tema,
                                            "estadisticas": estadisticas})
                continue
        elif "updated" in entry.keys():
            if "-" in entry.updated:
                lista1_elems_fecha_articulo = entry.updated.split("T")
                lista_elems_fecha_articulo = list()
                for elem in lista1_elems_fecha_articulo:
                    lista_elems_fecha_articulo.extend(elem.split("-"))
            else:
                lista_elems_fecha_articulo = entry.updated.split(" ")
            num_ocurrencias = 0
            for elemento in lista_elementos_fecha_actual:
                if len(elemento) == 1:
                    elemento = '0' + elemento
                for elem in lista_elems_fecha_articulo:
                    if elemento == elem:
                        num_ocurrencias += 1
            if num_ocurrencias == 3:
                puntaje, lista_conjunto_palabras, tema, estadisticas = \
                    determinar_importancia(titulo_noticia, contenido,
                                           link_noticia, peso)
                lista_diccionarios_entries.append({"titulo": titulo_noticia,
                                                   "link": link_noticia,
                                                   "puntaje": puntaje,
                                                   "conjunto_palabras":
                                                   lista_conjunto_palabras,
                                                  "tema": tema,
                                                   "estadisticas": estadisticas
                                                   })
    return lista_diccionarios_entries


def transformar():
    diccionario_noticias_fuentes = consultas_feed()
    for tupla in diccionario_noticias_fuentes.values():
        lista_entries = filtrar_contenido(tupla[0], tupla[1], tupla[2])
        diccionario_noticias_fuentes[tupla[0]] = lista_entries
    return diccionario_noticias_fuentes