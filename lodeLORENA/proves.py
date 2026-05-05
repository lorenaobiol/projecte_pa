import numpy as np
import pandas as pd
import csv

class GESTIONADOR():
    _matriu_dades:list

    def __init__(self):
        self._matriu_dades = []

    def importar_dades(self, nomfitxer,sep):
    
        usuari_index = dict()
        isbn_index = dict()
        matriu_dades = dict()

        with open(nomfitxer, "r", encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=sep)
            next(csv_reader)  

            for linia in csv_reader:
                user_id = int(linia[0])
                isbn = linia[1]
                rating = float(linia[2])

                if user_id not in usuari_index:
                    usuari_index[user_id] = len(usuari_index)

                if isbn not in isbn_index:
                    isbn_index[isbn] = len(isbn_index)

                fila = usuari_index[user_id]
                columna = isbn_index[isbn]

                if fila not in matriu_dades:
                    matriu_dades[fila] = dict()

                matriu_dades[fila][columna] = rating


