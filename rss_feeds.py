import feedparser
import json
import datetime


def cargar_filtros():
    """FUNCIÓN QUE RETORNA EL DICCIONARIO DE FILTROS DE Filtros_FinTech.json"""
    with open("Filtros_FinTech.json", 'r', encoding="utf-8") as filtros_file:
        diccionario_filtros = json.load(filtros_file)
        return diccionario_filtros


def cargar_fuentes():
    """FUNCIÓN QUE RETORNA EL DICCIONARIO DE LAS FUENTES DE NOTICIAS DE
    fuentes_rss.json"""
    with open("fuentes_rss.json", 'r', encoding="utf-8") as fuentes_file:
        diccionario_fuentes = json.load(fuentes_file)
        return diccionario_fuentes


def determinar_estadisticas(palabras_fintech):
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
            str_estadisticas += str(str(lista[0]) + ": "+str(lista[1])+"%")
        else:
            str_estadisticas += str(str(lista[0])+": "+str(lista[1])+"%"", ")
    return str_estadisticas


def determinar_tema(palabras_fintech_titulo, palabras_fintech_contenido):
    diccionario_temas = {"DLT": ["dlt", "blockchain", "distributed ledger",
                                 "descentralized ledger", "centralized ledger",
                                 "ethereum", "ripple", "digital asset",
                                 "hyperledger"], "Banca Abierta":
                                 ["open banking", "banca abierta"],
                         "Criptoactivos": ["criptomoneda", "cryptocurrency",
                                           "criptoactivo"], "Ciberseguridad": [
            "ciberseguridad", "cybersecurity", "ciberataque", "cyberattack"],
                         "Pagos Digitales": ["pago digital", "digital payment"]
        , "Monitoreo Tecnológico": ["suptech", "regtech", "regulatorio",
                                    "regulatory", "regulation", "regulación",
                                    "regulators", "reguladores"], "Big Data":
                             ["big data"], "CBDC": ["cbdc", "project jasper",
                             "project stella", "project ubin", "project khokha"
                             , "e-peso"], "Otro": ["inteligencia artificial",
                              "artificial intelligence", "ai",
                              "machine learning"]}

    for eje in diccionario_temas.keys():
        for palabra in diccionario_temas[eje]:
            if len(palabras_fintech_titulo) > 0:
                for palabra_fintech_titulo in palabras_fintech_titulo:
                    if palabra_fintech_titulo == palabra:
                        return eje
    lista_estadisticas_ejes = list()
    for eje in diccionario_temas.keys():
        suma_eje = 0
        for palabra_eje in diccionario_temas[eje]:
            for palabra_mencionada in palabras_fintech_contenido:
                if palabra_eje == palabra_mencionada:
                    suma_eje += 1
        lista_estadisticas_ejes.append([str(eje), suma_eje])
    lista_estadisticas_ejes = sorted(lista_estadisticas_ejes,
           key=lambda k: int(k[1]))
    return lista_estadisticas_ejes[-1][0]


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
    lista_listas_conjuntos_palabras = diccionario_filtros["conjuntos_palabras"]
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Se separan las palabras del titulo y del contenido y se ponen en sus
    # listas respectivas
    lista_palabras_titulo = titulo.split(" ")
    lista_palabras_contenido = contenido.strip(",").split(" ")
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Lista a la que se le agregan las palabras FinTech presentes en el
    # articulo
    lista_palabras_fintech_presentes = list()
    lista_indices_palabras_fintech_presentes = list()
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    """PRIMER FILTRO: DE PRESENCIA DE PALABRAS FINTECH EN TITULO
    SE DEBE DAR UN PUNTAJE BASE A LA NOTICIA BAJO ESTE CRITERIO"""
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

    """SEGUNDO FILTRO:SE SUMA UN PUNTAJE POR CADA MENCIÓN DE UNA PALABRA
    FINTECH PERO ÉSTE ES RELATIVO A LA POSICION DE LA PALABRA EN EL ARTICULO"""
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
                lista_palabras_fintech_presentes.append(
                    diccionario_palabra["palabra"])
                lista_indices_palabras_fintech_presentes.append(
                    indice_palabra_contenido)
        indice_palabra_contenido += 1

    """TERCER FILTRO: SE LE SUMA UN PUNTAJE ELEVADO A LA NOTICIA SI ES QUE
    MENCIONA CONJUNTOS DE PALABRAS ESPECIFICAS DEFINIDAS EN LA LISTA
    lista_palabras_contenido"""
    # La variable puntaje_conjunto_palabras representa la suma total de
    # puntajes por mención de conjuntos de palabras en el articulo
    puntaje_conjunto_palabras = 0
    lista_conjunto_palabras_mencionadas = list()
    for conjunto_palabras in diccionario_filtros["conjuntos_palabras"]:
        # En la siguiente linea se revisa si el el conjunto_palabras está en
        # la lista lista_palabras_fintech_presentes
        resultado = all(elem in lista_palabras_fintech_presentes for elem
                        in conjunto_palabras)
        if resultado:
            # Aqui se le suma un puntaje (**** POR DETERMINAR ****) si el
            # conjunto_palabras está presente en la lista
            # lista_palabras_fintech_presentes
            puntaje_conjunto_palabras += 100
            lista_conjunto_palabras_mencionadas.append(conjunto_palabras)
    puntaje += puntaje_conjunto_palabras

    """FILTRO POR AUTORES (FALTA DEFINIR AUTORES)
    for diccionario_autor in lista_diccionarios_autores:
        if diccionario_autor["nombre"] == autor:
            puntaje += diccionario_autor["peso"]
    """
    str_estadisticas = determinar_estadisticas(lista_palabras_fintech_presentes)
    tema_global_noticia = determinar_tema(lista_palabras_titulo, lista_palabras_fintech_presentes)
    return puntaje, lista_conjunto_palabras_mencionadas, tema_global_noticia, str_estadisticas


def filtrar_contenido(nombre_fuente, contenido, peso):
    """AQUI SE ENCUENTRAN TODOS LOS FILTROS"""
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
        """La llave published no siempre existe en el diccionario entregado por
         el RSS feed por lo que se debe tomar en cuenta la llave updated"""
        if "published" in entry.keys():
            lista_elems_fecha_articulo = entry.published.split(" ")
            num_ocurrencias = 0
            for elemento in lista_elementos_fecha_actual:
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
            lista_elems_fecha_articulo = entry.updated.split(" ")
            num_ocurrencias = 0
            for elemento in lista_elementos_fecha_actual:
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


def crear_recopilación_top_noticias(diccionario_fuentes_noticias):
    """FUNCIÓN QUE ESCRIBE EN UN DOCUMENTO .txt LAS MEJORES NOTICIAS DEL DÍA"""
    with open("Recopilaciones/{}.txt".format(datetime.datetime.now().date()),
              "w") as recopilacion_del_dia_file:
        lista_todas_las_noticias = list()
        for fuente in diccionario_fuentes_noticias.keys():
            # Se ordena la lista de noticias respectiva a cada fuente según su
            # puntaje
            for noticia in diccionario_fuentes_noticias[fuente]:
                lista_todas_las_noticias.append(noticia)
        lista_ordenada_todas_las_noticias = sorted(lista_todas_las_noticias,
                                            key=lambda k: int(k['puntaje']))
        top_30_noticias = lista_ordenada_todas_las_noticias[-30::]
        temas_ejes = ["DLT", "Criptoactivos", "Ciberseguridad",
                         "Pagos Digitales", "Monitoreo Tecnológico", "Big Data"
                    , "CBDC", "Banca Abierta","Otro"]
        for eje in temas_ejes:
            recopilacion_del_dia_file.write(str(eje)+"\n"+"\n")
            indice_lista_top_30 = 0
            for noticia in top_30_noticias:
                if noticia["tema"] == eje:
                    del top_30_noticias[indice_lista_top_30]
                    recopilacion_del_dia_file.write(noticia["titulo"]+" {"+
                                                    noticia["estadisticas"]+"} "+"\n"+
                                                    noticia["link"]+"\n"+str(
                                                    noticia["puntaje"])+"\n"+"\n")
                indice_lista_top_30 += 1
        if len(top_30_noticias) > 0:
            for noticia in top_30_noticias:
                recopilacion_del_dia_file.write(noticia["titulo"] + " {" +
                                                noticia[
                                                    "estadisticas"] + "} " + "\n" +
                                                noticia[
                                                    "link"] + "\n" + str(
                    noticia["puntaje"]) + "\n" + "\n")


def consultas_feed():
    diccionario_fuentes = cargar_fuentes()
    # La variable diccionario_noticias_fuentes es un diccionario en el que cada
    # key es el nombre de una fuente y cada valor respectivo a una key es una
    # lista de noticias que tienen un determinado puntaje (>0 o un top número
    # de noticias)
    diccionario_noticias_fuentes = dict()
    # ------------------------------------------------------------------------
    for diccionario_fuente in diccionario_fuentes["fuentes"]:
        nombre = diccionario_fuente["nombre"]
        print(nombre)
        url = diccionario_fuente["url"]
        peso = diccionario_fuente["peso"]
        url_content = feedparser.parse(url)
        lista_entries = filtrar_contenido(nombre, url_content, peso)
        diccionario_noticias_fuentes[nombre] = lista_entries
    crear_recopilación_top_noticias(diccionario_noticias_fuentes)


if __name__ == '__main__':
    consultas_feed()



