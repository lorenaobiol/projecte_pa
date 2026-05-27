from abc import ABC, abstractmethod
from typing import List, Dict
import csv
from contingut import *
from config import *
import numpy as np
import logging


#gestionador BOOKS
class Gestionador:
    """Classe que gestiona les dades del sistema de recomanació.
 
    S'encarrega d'importar, emmagatzemar i proporcionar accés a la matriu de
    valoracions, el diccionari de continguts i els índexos d'usuaris i continguts.
 
    Attributes:
        _matriu_dades (np.ndarray): Matriu de valoracions (usuaris x continguts).
        _dict_contingut (Dict[str, Contingut]): Diccionari que mapeja l'ID de cada
            contingut amb el seu objecte Contingut corresponent.
        _usuari_index (Dict[int, int]): Diccionari que mapeja l'ID real de cada
            usuari amb la seva fila a la matriu de dades.
        _contingut_index (Dict[str, int]): Diccionari que mapeja l'ID real de cada
            contingut amb la seva columna a la matriu de dades.
        _tipus_contingut (str): Tipus de contingut del sistema ('MOVIES' o 'BOOKS').
    """

    _matriu_dades: list
    _dict_contingut: Dict[str, 'Contingut']
    _usuari_index: Dict[int, int]
    _contingut_index: Dict[str, int]
    _tipus_contingut: str

    def __init__(self, tipus_contingut: str):
        """Inicialitza el gestionador amb el tipus de contingut especificat.
 
        Args:
            tipus_contingut (str): Tipus de contingut del sistema. Valors possibles:
                'MOVIES' per a pel·lícules, 'BOOKS' per a llibres.
        """
        self._matriu_dades = []
        self._dict_contingut = {}
        self._usuari_index  = {}
        self._contingut_index = {}
        self._tipus_contingut = tipus_contingut
        logging.info(f"Inicialització del gestionador per al tipus de contingut: {tipus_contingut}")


    def get_matriu_dades(self): 
        """Retorna la matriu de valoracions dels usuaris.
 
        Returns:
            np.ndarray: Matriu de forma (num_usuaris x num_continguts) amb les valoracions.
        """
        return self._matriu_dades
    def get_dict_contingut(self): 
        """Retorna el diccionari de continguts del sistema.
 
        Returns:
            Dict[str, Contingut]: Diccionari que mapeja l'ID de cada contingut
                amb el seu objecte Contingut corresponent.
        """
        return self._dict_contingut
    def get_usuari_index(self): 
        """Retorna el diccionari d'índexos d'usuaris.
 
        Returns:
            Dict[int, int]: Diccionari que mapeja l'ID real de cada usuari
                amb la seva fila a la matriu de dades.
        """
        return self._usuari_index
    def get_contingut_index(self): 
        """Retorna el diccionari d'índexos de continguts.
 
        Returns:
            Dict[str, int]: Diccionari que mapeja l'ID real de cada contingut
                amb la seva columna a la matriu de dades.
        """
        return self._contingut_index
    def get_tipus_contingut(self):
        """Retorna el tipus de contingut del sistema.
 
        Returns:
            str: Tipus de contingut ('MOVIES' o 'BOOKS').
        """
        return self._tipus_contingut

    def importar_dades(self, nomfitxer,sep):
        """Importa les valoracions dels usuaris des d'un fitxer CSV i construeix la matriu de dades.
 
        Llegeix el fitxer de valoracions, assigna índexos interns a usuaris i continguts,
        i construeix la matriu numpy de valoracions. Per a BOOKS, només importa fins al
        límit definit per la constant LIMIT.
 
        Args:
            nomfitxer (str): Nom del fitxer CSV amb les valoracions.
            sep (str): Separador de columnes del fitxer CSV.
 
        Example:
            gestionador = Gestionador('MOVIES')
            gestionador.importar_dades('ratings.csv', ',')
        """

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
        """Importa la informació dels continguts des d'un fitxer CSV.
 
        Per a MOVIES, importa l'identificador, el títol i els gèneres de cada pel·lícula.
        Per a BOOKS, només importa els llibres que ja apareixen a l'índex de continguts
        (és a dir, que tenen almenys una valoració).
 
        Args:
            nomfitxer (str): Nom del fitxer CSV amb la informació dels continguts.
            sep (str): Separador de columnes del fitxer CSV.
 
        Example:
            gestionador = Gestionador('BOOKS')
            gestionador.importar_dades('ratings.csv', ';')
            gestionador.importar_dades_contingut('books.csv', ';')
        """

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


    
    
   