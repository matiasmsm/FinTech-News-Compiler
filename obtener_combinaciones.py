import json


def obtener_combinaciones():
    with open("Filtros_FinTech.json", "r") as filtros_file:
        diccionario_filtros_fintech = json.load(filtros_file)
        listado_palabras = diccionario_filtros_fintech["palabras"]
    lista_combinaciones = list()
    for dict_palabra in listado_palabras:
        palabra = dict_palabra["palabra"]
        lista_combinaciones.append([palabra])
        for dict_palabra in listado_palabras:
            if dict_palabra["palabra"] != palabra:
                if [palabra, dict_palabra["palabra"]] in lista_combinaciones or [dict_palabra["palabra"], palabra] in lista_combinaciones:
                    continue
                else:
                    lista_combinaciones.append([palabra, dict_palabra["palabra"]])
    diccionario_nuevo_json = {"combinaciones": lista_combinaciones}
    with open("combinaciones_palabras.json", "w") as combinaciones_file:
        json.dump(diccionario_nuevo_json, combinaciones_file)

obtener_combinaciones()