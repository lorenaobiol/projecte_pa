from contingut import *
from config import *
from recomanacio import *
from gestionador import *
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict
from math import sqrt

logging.basicConfig(

    filename='log '+ get_data() +'.txt',
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    #handlers= [logging.FileHandler('log '+ get_data() +'.txt'), 
              #logging.StreamHandler()] 
    )

class Avaluacio(ABC):
    """
    Classe abstracta per avaluar la qualitat d'un sistema de recomanació.
    Compara les puntuacions recomanades amb les puntuacions reals de l'usuari
    mitjançant les mètriques MAE i RMSE.

    """

    _resultat_MAE: float
    _resultat_RMSE: float
    _recomanador: Recomanacio
    _punt_usuari: List

    def __init__(self, recomanador:Recomanacio, iduser:int, gestionador:Gestionador):
        """
        Inicialitza l'avaluació amb el recomanador, l'identificador de l'usuari
        i el gestionador de dades. Obté les puntuacions reals de l'usuari.

        """

        logging.debug(f"Inicialitzant Avaluacio per usuari {iduser}")

        self._resultat_MAE = 0
        self._resultat_RMSE = 0
        self._recomanador=recomanador
        self._gestionador=gestionador
        self._punt_usuari=gestionador.get_matriu_dades()[gestionador.get_usuari_index()[iduser],:]
        
        logging.debug(f"Puntuacions de l'usuari carregades: {self._punt_usuari}")

    def calcular_MAE(self):
        """
        Calcula el Mean Absolute Error (MAE) entre les puntuacions recomanades
        i les puntuacions reals de l'usuari. Només té en compte els ítems
        que l'usuari ha puntuat (puntuació != 0).

        """

        self._recomanador.calcular_recomanacio(mode_avaluacio=True)
        dict_recomanacio = self._recomanador.get_recomanacio_final()
        
        sumatori = 0
        items_avaluats = 0
        for idcont, p_reco in dict_recomanacio.items():
            columna = self._gestionador.get_contingut_index()[idcont]
            p_usuari = self._punt_usuari[columna]
        
            if p_usuari != 0:
                sumatori += abs(p_reco - p_usuari)
                items_avaluats += 1

        self._resultat_MAE = sumatori / items_avaluats if items_avaluats > 0 else 0
        logging.info(f"MAE calculat: {self._resultat_MAE}")
        
        return self._resultat_MAE
    
    def calcular_RMSE(self):
        """
        Calcula el Root Mean Square Error (RMSE) entre les puntuacions recomanades
        i les puntuacions reals de l'usuari. Penalitza més els errors grans.
        Només té en compte els ítems que l'usuari ha puntuat (puntuació != 0).

        """

        self._recomanador.calcular_recomanacio(mode_avaluacio=True)
        dict_recomanacio=self._recomanador.get_recomanacio_final()

        sumatori = 0
        items_avaluats = 0
        for idcont, p_reco in dict_recomanacio.items():
            columna = self._gestionador.get_contingut_index()[idcont]
            p_usuari = self._punt_usuari[columna]

            if p_usuari != 0:  #sol sagafen les q son diferents d zero? ala diapositiva diu q les agafa totes
                sumatori += (p_reco - p_usuari) ** 2 
                items_avaluats += 1

        self._resultat_RMSE = sqrt(sumatori / items_avaluats) if items_avaluats > 0 else 0
        logging.info(f"RMSE calculat: {self._resultat_RMSE}")
        return self._resultat_RMSE
    
    def __str__(self) -> str:
        """
        Retorna una cadena de text amb el resultat de l'avaluació calculada.
        Si no s'ha calculat cap mètrica, ho indica.

        """

        if self._resultat_MAE != 0:
            logging.debug(f"Retornant MAE: {self._resultat_MAE}")
            return f"MAE: {self._resultat_MAE}"
        elif self._resultat_RMSE != 0: 
            logging.debug(f"Retornant RMSE: {self._resultat_RMSE}")
            return f"RMSE: {self._resultat_RMSE}"
        logging.warning("No s'ha calculat cap avaluació")
        return 'No es pot avaluar'
        