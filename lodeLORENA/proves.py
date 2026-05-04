import numpy as np
import pandas as pd

class Gestionador():
    _matru_dades:list

    def __init__(self):
        self._matru_dades = []

    def importar_dades(self, nomfitxer,sep):
        
        data=pd.read_csv(nomfitxer, sep)

        usuaris_unics = data['User-ID'].unique()
        isbns_unics = data['ISBN'].unique()

        usuari_index=dict()
        for i in range(len(usuaris_unics)):
            usuari_index[usuaris_unics[i]] = i

        isbn_index=dict()
        for i in range(len(isbns_unics)):
            isbn_index[isbns_unics[i]] = i

        matriu_dades=np.zeros((len(usuaris_unics), len(isbns_unics)))

        with open("Ratings.csv", "r") as f: 
            next(f)
            for linia in f:
                camps = linia.strip().split(",")
                user_id = int(camps[0])
                isbn = camps[1]
                rating = float(camps[2])

                fila=usuari_index[user_id]
                columna=isbn_index[isbn]

                matriu_dades[fila, columna] = rating

        print(matriu_dades.head(3))

        #me dona esre error: numpy._core._exceptions._ArrayMemoryError: Unable to allocate 267. GiB for an array with shape (105283, 340556) and data type float64
        #com puc fer que ocupe menys memoria?

