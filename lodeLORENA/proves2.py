import pandas as pd
import numpy as np

data=pd.read_csv("Ratings.csv", sep=",")

print(data.head(3))

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

