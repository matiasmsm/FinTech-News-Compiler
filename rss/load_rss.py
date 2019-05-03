import datetime

from .RSS.transform_rss import transformar


def crear_recopilación_top_noticias():
    """FUNCIÓN QUE ESCRIBE EN UN DOCUMENTO .txt LAS MEJORES NOTICIAS DEL DÍA"""
    diccionario_fuentes_noticias = transformar()
    with open("Recopilaciones/{}.txt".format(datetime.datetime.now().date()),
              "w") as recopilacion_del_dia_file:
        lista_todas_las_noticias = list()
        for fuente in diccionario_fuentes_noticias.keys():
            # Se ordena la lista de noticias respectiva a cada fuente según su
            # puntaje
            lista_links_noticias = list()
            for noticia in diccionario_fuentes_noticias[fuente]:
                # Se revisa si la noticia no está repetida
                if noticia["link"] not in lista_links_noticias:
                    lista_links_noticias.append(noticia["link"])
                    lista_todas_las_noticias.append(noticia)
        lista_ordenada_todas_las_noticias = sorted(lista_todas_las_noticias,
                                            key=lambda k: int(k['puntaje']))
        top_noticias = [n for n in lista_ordenada_todas_las_noticias if n[
            'puntaje'] > 0]
        temas_ejes = ["DLT", "Criptoactivos", "Ciberseguridad",
                         "Pagos Digitales", "Monitoreo Tecnológico", "Big Data"
                    , "CBDC", "Banca Abierta","Otro"]
        lista_links_noticias_incluidas = list()
        for eje in temas_ejes:
            recopilacion_del_dia_file.write(str(eje)+"\n"+"\n")
            indice_lista_top = 0
            for noticia in top_noticias:
                if noticia["tema"] == eje and noticia["link"] not in lista_links_noticias_incluidas:
                    del top_noticias[indice_lista_top]
                    lista_links_noticias_incluidas.append(noticia["link"])
                    recopilacion_del_dia_file.write(noticia["titulo"]+" {"+
                                                    noticia["estadisticas"]+"}"+"\n"+
                                                    noticia["link"]+"\n"+str(
                                                    noticia["puntaje"])+"\n"+"\n")
                indice_lista_top += 1
        if len(top_noticias) > 0:
            for noticia in top_noticias:
                recopilacion_del_dia_file.write(noticia["titulo"] + " {" +
                                                noticia[
                                                    "estadisticas"] + "} " + "\n" +
                                                noticia[
                                                    "link"] + "\n" + str(
                    noticia["puntaje"]) + "\n" + "\n")
