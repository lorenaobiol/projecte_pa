from abc import ABC, abstractmethod
from typing import List, Dict
import csv
from contingut import *
from config import *
import numpy as np
import logging

logging.basicConfig(

    filename='log '+ get_data() +'.txt',
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    #handlers= [logging.FileHandler('log '+ get_data() +'.txt'), 
              #logging.StreamHandler()] 
    )

#gestionador BOOKS
class Gestionador:

    _matriu_dades: list
    _dict_contingut: Dict[str, 'Contingut']
    _usuari_index: Dict[int, int]
    _contingut_index: Dict[str, int]
    _tipus_contingut: str

    def __init__(self, tipus_contingut: str):
        self._matriu_dades = []
        self._dict_contingut = {}
        self._usuari_index  = {}
        self._contingut_index = {}
        self._tipus_contingut = tipus_contingut
        logging.info(f"Inicialització del gestionador per al tipus de contingut: {tipus_contingut}")


    def get_matriu_dades(self): return self._matriu_dades
    def get_dict_contingut(self): return self._dict_contingut
    def get_usuari_index(self): return self._usuari_index
    def get_contingut_index(self): return self._contingut_index
    def get_tipus_contingut(self): return self._tipus_contingut

    def importar_dades(self, nomfitxer,sep):

        usuari_index = dict()
        idcont_index = dict()
        matriu_dades = dict()
        path="./dataset/"
        if self._tipus_contingut == 'MOVIES':
            path+="MoviesLens100k/"
        else:
            path+="Books/"
        
        with open(path+nomfitxer, "r", encoding='utf-8') as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=sep)
            next(csv_reader)

            for linia in csv_reader:
                #if books contorolar els 10.000 primers

                user_id = int(linia[0])
                idcont = int(linia[1]) if self._tipus_contingut == 'MOVIES' else linia[1]
                rating = float(linia[2])

                if user_id not in usuari_index:
                    usuari_index[user_id] = len(usuari_index)

                if idcont not in idcont_index:

                    if self._tipus_contingut == 'BOOKS':
                        if len(idcont_index) >= LIMIT:
                            continue

                    idcont_index[idcont] = len(idcont_index)

                fila = usuari_index[user_id]
                columna = idcont_index[idcont]

                if fila not in matriu_dades:
                    matriu_dades[fila] = dict()

                matriu_dades[fila][columna] = rating

        num_usuaris = len(usuari_index)
        num_items = len(idcont_index)

        self._matriu_dades = np.zeros((num_usuaris, num_items), dtype=np.float32)

        for f, columnes in matriu_dades.items():
            for c, valor_rating in columnes.items():
                self._matriu_dades[f, c] = valor_rating

        self._usuari_index = usuari_index
        self._contingut_index = idcont_index
        logging.info(f"Dades importades des de {nomfitxer}. Nombre d'usuaris: {num_usuaris}, Nombre de continguts: {num_items}")
        logging.info(f"Diccionaris i matriu de dades creada correctament amb forma: {self._matriu_dades.shape}")

    def importar_dades_contingut(self, nomfitxer,sep):
        path="./dataset/"
        if self._tipus_contingut == 'MOVIES':
            path+="MoviesLens100k/"
        else:
            path+="Books/"

        with open(path+nomfitxer, "r", encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=sep)
            next(csv_reader)  

            if self._tipus_contingut == 'MOVIES':
                for linia in csv_reader:
                    movieid= int(linia[0])
                    titol = linia[1]
                    generes = linia[2].split('|') 

                    contingut=Movie(movieid,titol,generes)

                    self._dict_contingut[movieid]=contingut
            
            elif self._tipus_contingut == 'BOOKS':
                #associar usuaris als llibres
                for linia in csv_reader:
                    isbn = linia[0]
                    if isbn in self._contingut_index:  # només importar contingut que existeix a les valoracions
                        titol = linia[1]
                        autor = linia[2]
                        any_publicacio = int(linia[3])

                        contingut=Llibre(isbn,titol,autor,any_publicacio)

                        self._dict_contingut[isbn]=contingut
        logging.info(f"Dades de contingut importades des de {nomfitxer}. Nombre de continguts: {len(self._dict_contingut)}")
        logging.info("Diccionari de contingut creat correctament")

    def mostrar_punutacions_usuari(self, iduser:int):

        fila=self._usuari_index[iduser]

        for contingut, columna in self._contingut_index.items():
            valor_rating=self._matriu_dades[fila, columna]
            print('Continugut:',contingut, 'Puntuació:',valor_rating)
    
    
    
    
   