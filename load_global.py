import smtplib
import RSS.transform_rss
import datetime
import PyMediaRSS2Gen
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY
from control_versiones_automatico_gitpython import subir_version


def juntar_datos(diccionario_noticias):
    TEXTO = ""
    lista_todas_las_noticias = list()
    lista_contenido = list()
    lista_links_noticias = list()
    lista_titulos_noticias = list()
    for fuente in diccionario_noticias.keys():
        # Se ordena la lista de noticias respectiva a cada fuente según su
        # puntaje
        for noticia in diccionario_noticias[fuente]:
            # Se revisa si la noticia no está repetida
            if noticia["link"] not in lista_links_noticias:
                porcentaje_coincidencia = 0
                for titulo in lista_titulos_noticias:
                    for palabra_titulo in list(noticia["titulo"]):
                        for palabra_titulo_lista_titulos_noticias in list(
                                titulo):
                            if palabra_titulo == \
                                    palabra_titulo_lista_titulos_noticias:
                                porcentaje_coincidencia += 1
                porcentaje_coincidencia = porcentaje_coincidencia/len(list(
                    noticia["titulo"]))
                if porcentaje_coincidencia < 80:
                    lista_links_noticias.append(noticia["link"])
                    lista_todas_las_noticias.append(noticia)
    lista_ordenada_todas_las_noticias = sorted(lista_todas_las_noticias,
                                               key=lambda k: int(k['puntaje']))
    top_noticias = [n for n in lista_ordenada_todas_las_noticias if n[
        'puntaje'] > 0]
    temas_ejes = ["DLT", "Criptoactivos", "Ciberseguridad",
                  "Pagos Digitales", "Monitoreo Tecnológico", "Big Data"
        , "CBDC", "Banca Abierta", "Otro"]
    diccionario_contenido_noticias = dict()
    for eje in temas_ejes:
        TEXTO += (str(eje) + "\n" + "\n")
        lista_contenido.append(eje)
        indice_lista_top = 0
        diccionario_contenido_noticias[eje] = list()
        for noticia in top_noticias:
            if noticia["tema"] == eje:
                del top_noticias[indice_lista_top]
                TEXTO += noticia["titulo"] + " {" + noticia["estadisticas"] + \
                         "}" + "\n" +noticia["link"] + "\n" + \
                         str(noticia["puntaje"]) + "\n" + "\n"
                lista_contenido.append(noticia["titulo"] + " {" + noticia[
                    "estadisticas"] +\
                         "}")
                lista_contenido.append(noticia["link"])
                diccionario_contenido_noticias[eje].append(noticia)
            indice_lista_top += 1
    if len(top_noticias) > 0:
        for noticia in top_noticias:
            TEXTO += (noticia["titulo"] + " {" +
                                            noticia[
                                                "estadisticas"] + "} " + "\n" +
                                            noticia[
                                                "link"] + "\n" + str(
                noticia["puntaje"]) + "\n" + "\n")
            lista_contenido.append(noticia["titulo"] + " {" +
                                            noticia[
                                                "estadisticas"] + "} ")
            lista_contenido.append(noticia["link"])
            diccionario_contenido_noticias["Otro"].append(noticia)
    return TEXTO, lista_contenido, diccionario_contenido_noticias


def enviar_mail(contenido):
    SERVER = ""
    FROM = "mmingo@bcch.local"
    TO = ["lsanz@bcentral.cl", "mamusa@bcentral.cl"]
    SUBJECT = "Noticias {}".format(datetime.datetime.now().date())
    message = """From: {}\r\nTo: {}\r\nSubject: {}\r\n

    {}
    """.format(FROM, ",".join(TO), SUBJECT, contenido)
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)


def escribir_pdf(lista_contenido):
    doc = SimpleDocTemplate("Recopilaciones PDF/Noticias {}.pdf".format(
        datetime.datetime.now().date()), pagesize=letter)
    width, height = letter
    Story = []
    logo = "Fotos/logo_bcch.png"
    im = Image(logo, inch, inch)
    Story.append(im)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    titulo = "Noticias {}".format(datetime.datetime.now().date())
    ptext = '<font size=12>%s</font>'%titulo
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    for linea in lista_contenido:
        ptext = '<font size=12>%s</font>'%linea
        Story.append(Paragraph(ptext, styles["Normal"]))
        if linea[:4] != ["h", "t", "t", "p"]:
            Story.append(Spacer(1, 12))
    doc.build(Story)


def crear_txt(contenido):
    """FUNCIÓN QUE ESCRIBE EN UN DOCUMENTO .txt LAS MEJORES NOTICIAS DEL DÍA"""
    with open("Recopilaciones/{}.txt".format(datetime.datetime.now().date()),
              "w") as recopilacion_del_dia_file:
        recopilacion_del_dia_file.write(contenido)


def escribir_html(lista_palabras):
    head_html="""<html>
<head></head>
<body>\n"""
    head_html += """</body>\n</html>"""
    with open("resultado.html", "w") as html_file:
        html_file.write(head_html)


def escribir_rss_xml(diccionario_contenido_noticias):
    mediaFeed = PyMediaRSS2Gen.MediaRSS2(
        title="Noticias FinTech",
        link="https://github.com/unknomads/Recopilador-de-Noticias",
        description="Noticias FinTech recopiladas durante el día."
    )
    mediaFeed.copyright = "Copyright (c) 2019 Banco Central de Chile. All rights reserved."
    mediaFeed.lastBuildDate = datetime.datetime.now()
    mediaFeed.items = list()
    for key, value in diccionario_contenido_noticias.items():
        for noticia in value:
            mediaFeed.items.append(PyMediaRSS2Gen.MediaRSSItem(
                title=str(noticia["fuente"])+": "+noticia["titulo"]+" - "+" Puntaje: "+str(noticia["puntaje"]),
                link=noticia["link"],
                description=noticia["summary"],
                pubDate=noticia["pubDate"]
            ))
    mediaFeed.write_xml(open("feed_rss.xml", "w"))


def load_todo():
    diccionario_fuentes_noticias_rss = RSS.transform_rss.transformar()
    contenido, lista_contenido, diccionario_contenido_noticias = juntar_datos(diccionario_fuentes_noticias_rss)
    escribir_pdf(lista_contenido)
    crear_txt(contenido)
    escribir_rss_xml(diccionario_contenido_noticias)
    subir_version()