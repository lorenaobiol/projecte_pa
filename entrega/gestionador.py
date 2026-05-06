from abc import ABC, abstractmethod
from typing import List, Dict
import csv
from entrega.contingut import Contingut
from entrega.usuari import Usuari
import numpy as np


#gestionador BOOKS
class Gestionador_BOOKS:

    _matriu_dades: list
    _dict_contingut: Dict[str, 'Contingut']
    _dict_usuaris: Dict[int, 'Usuari']
    _usuari_index: Dict[int, int]
    _contingut_index: Dict[str, int]

    def __init__(self):
        self._matriu_dades = []
        self._dict_contingut = {}
        self._dict_usuaris = {}
        self._usuari_index  = {}
        self._contingut_index = {}

    def get_matriu_dades(self): 
        return self._matriu_dades
    def get_dict_contingut(self): 
        return self._dict_contingut
    def get_dict_usuaris(self): 
        return self._dict_usuaris
    def get_usuari_index(self): 
        return self._usuari_index
    def get_contingut_index(self): 
        return self._contingut_index

    
    def importar_dades(self, nomfitxer,sep):
    
        usuari_index = dict()
        idcont_index = dict()
        matriu_dades = dict()

        with open(nomfitxer, "r", encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=sep)
            next(csv_reader)  

            for linia in csv_reader:
                user_id = int(linia[0])
                idcont = linia[1]
                rating = float(linia[2])

                if user_id not in usuari_index:
                    usuari_index[user_id] = len(usuari_index)

                if idcont not in idcont_index:
                    idcont_index[idcont] = len(idcont_index)

                fila = usuari_index[user_id]
                columna = idcont_index[idcont]

                if fila not in matriu_dades: #matriu dades a matriu
                    matriu_dades[fila] = dict()

                matriu_dades[fila][columna] = rating
        
        # 2. ARA SÍ: Creem la matriu NumPy de veritat
        num_usuaris = len(usuari_index)
        num_items = len(idcont_index)
    
        print(f"Creant matriu NumPy de dimensions: {num_usuaris}x{num_items}...")
    
    # Utilitzem float32 per estalviar la meitat de memòria RAM (en comptes del float64 per defecte)
        self.matriu_dades = np.zeros((num_usuaris, num_items), dtype=np.float32)

    # 3. Traspassem les dades del diccionari temporal a la matriu NumPy
        for f, columnes in matriu_dades.items():
            for c, valor_rating in columnes.items():
                self.matriu_dades[f, c] = valor_rating

    
        self.usuari_index = usuari_index
        self.idcont_index = idcont_index

    #def importar_dades_contingut(self, nomfitxer,sep):
    #def importar_dades_usuaris(self, nomfitxer,sep):
    #getters

#gestionador MOVIES

class Gestionador_MOVIES: