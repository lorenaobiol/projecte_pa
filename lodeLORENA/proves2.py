import pandas as pd
import numpy as np

data=pd.read_csv('Ratings.csv', sep=',')

usuaris_unics = data['User-ID'].unique()
isbns_unics = data['ISBN'].unique()

usuari_index=dict()
for i,usuaris in enumerate(usuaris_unics):
    usuari_index[usuaris] = i

isbn_index=dict()
for i in range(len(isbns_unics)):
    isbn_index[isbns_unics[i]] = i

matriu_dades=dict()

with open("Ratings.csv", "r") as f: 
    next(f)
    for linia in f:
        camps = linia.strip().split(",")  #######
        user_id = int(camps[0])
        isbn = camps[1]
        rating = float(camps[2])

        fila=usuari_index[user_id]
        columna=isbn_index[isbn]

        if fila not in matriu_dades:
            matriu_dades[fila] = dict()

        matriu_dades[fila][columna] = rating

list(matriu_dades.keys())[0]

