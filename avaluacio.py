from contingut import *
from config import *
from recomanacio import *
from gestionador import *
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict
from math import sqrt

class Avaluacio(ABC):

    _resultat_MAE: float
    _resultat_RMSE: float
    _recomanador: Recomanacio
    _punt_usuari: List

    def __init__(self, recomanador:Recomanacio, iduser:int, gestionador:Gestionador):

        self._resultat_MAE = 0
        self._resultat_RMSE = 0
        self._recomanador=recomanador
        self._gestionador=gestionador
        self._punt_usuari=gestionador.get_matriu_dades()[gestionador.get_usuari_index()[iduser],:]

    def calcular_MAE(self):
        '''
        dict_recomanacio=self._recomanador.get_recomanacio_final()
        
        sumatori=sum(abs(p_reco-p_usuari) for  p_reco,p_usuari in zip(dict_recomanacio.values(),self._punt_usuari) if p_usuari != 0)
        items=[it for it in self._punt_usuari if it!=0]

        self._resultat_MAE=sumatori/len(items)

        return self._resultat_MAE'''

        
        cont_index = self._gestionador.get_contingut_index()
        recomanador = self._recomanador
        gestionador = self._gestionador

    # Recalculem prediccions per a items que l'usuari JA ha puntuat
        sumatori = 0
        items_avaluats = 0

        for idcont, columna in cont_index.items():
            p_usuari = self._punt_usuari[columna]
            if p_usuari == 0:
                continue  # Només avaluem el que ha vist

            # agafar les pelis que a ha vist
            p_reco = recomanador.get_recomanacio_final().get(idcont)
            if p_reco is None:
                continue

            sumatori += abs(p_reco - p_usuari)
            items_avaluats += 1

        self._resultat_MAE = sumatori / items_avaluats if items_avaluats > 0 else 0
        return self._resultat_MAE
    
    def calcular_RMSE(self):

        dict_recomanacio=self._recomanador.get_recomanacio_final()

        sumatori=sum((p_reco-p_usuari)**2 for  p_reco,p_usuari in zip(dict_recomanacio.values(),self._punt_usuari) if p_usuari != 0)
        items=[it for it in self._punt_usuari if it!=0]

        self._resultat_RMSE=sqrt(sumatori/len(items))

        return self._resultat_RMSE
    
    def __str__(self) -> str:

        if self._resultat_MAE != 0:
            return f"MAE: {self._resultat_MAE}"
        elif self._resultat_RMSE != 0: 
            return f"RMSE: {self._resultat_RMSE}"
        