import pinboard
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY


pb = pinboard.Pinboard('lsanz_observatorio:CC8E7F9E71CC9B935378')


def escribir_resumen_semanal():
    posts = pb.posts.recent(tag=["publishedOT", "d:201903"])
    lista_contenido = list()
    with open("Resumenes Semanales/resumen_semanal{}.txt".format(
            datetime.datetime.now()), "w") as resumen_semanal_file:
        for post in posts["posts"]:
            resumen_semanal_file.write(post.description+"\n")
            resumen_semanal_file.write(post.url + "\n \n")
            lista_contenido.append(post.description)
            lista_contenido.append(post.url)
    escribir_pdf(lista_contenido)


def escribir_pdf(lista_contenido):
    doc = SimpleDocTemplate("Resumenes Semanales/resumen_semanal{}.pdf".format(
            datetime.datetime.now()), pagesize=letter)
    width, height = letter
    Story = []
    logo = "Fotos/logo_bcch.png"
    im = Image(logo, inch, inch)
    Story.append(im)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    titulo = "Resumen Semanal Noticias FinTech"
    ptext = '<font size=12>%s</font>'%titulo
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    for linea in lista_contenido:
        ptext = '<font size=12>%s</font>'%linea
        Story.append(Paragraph(ptext, styles["Normal"]))
        if linea[:4] != ["h", "t", "t", "p"]:
            Story.append(Spacer(1, 12))
    doc.build(Story)

def feedPinboard(lista_contenido):
    doc = SimpleDocTemplate("Resumenes Semanales/resumen_semanal{}.pdf".format(
            datetime.datetime.now()), pagesize=letter)
    width, height = letter
    Story = []
    logo = "Fotos/logo_bcch.png"
    im = Image(logo, inch, inch)
    Story.append(im)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    titulo = "Resumen Semanal Noticias FinTech"
    ptext = '<font size=12>%s</font>'%titulo
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    for linea in lista_contenido:
        ptext = '<font size=12>%s</font>'%linea
        Story.append(Paragraph(ptext, styles["Normal"]))
        if linea[:4] != ["h", "t", "t", "p"]:
            Story.append(Spacer(1, 12))
    doc.build(Story)

if __name__ == '__main__':
    escribir_resumen_semanal()
