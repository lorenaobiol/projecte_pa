from entrega.contingut import *
from entrega.config import *
from entrega.recomanacio import *
from entrega.gestionador import *
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict
from math import abs,sqrt

class Avaluacio(ABC):

    _resultat_MAE: float
    _resultat_RMSE: float
    _recomanador: Recomanacio
    _punt_usuari: List

    def __init__(self, recomanador:Recomanacio, iduser:int, gestionador:Gestionador):

        self._resultat_MAE = 0
        self._resultat_RMSE = 0
        self._recomanador=recomanador
        self._punt_usuari=gestionador.get_matriu_dades()[gestionador.get_usuari_index()[iduser],:]

    def calcular_MAE(self):

        dict_recomanacio=self._recomanador.get_recomanacio_final()
        
        sumatori=sum(abs(p_reco-p_usuari) for  p_reco,p_usuari in zip(dict_recomanacio.values(),self._punt_usuari) if p_usuari != 0)
        items=[it for it in self._punt_usuari if it!=0]

        self._resultat_MAE=sumatori/len(items)

        return self._resultat_MAE
    
    def calcular_RMSE(self):

        dict_recomanacio=self._recomanador.get_recomanacio_final()

        sumatori=sum((p_reco-p_usuari)**2 for  p_reco,p_usuari in zip(dict_recomanacio.values(),self._punt_usuari) if p_usuari != 0))
        items=[it for it in self._punt_usuari if it!=0]

        self._resultat_RMSE=sqrt(sumatori/len(items))

        return self._resultat_RMSE
    
    def __str__(self) -> str:

        if self._resultat_MAE != 0:
            return f"MAE: {self._resultat_MAE}"
        elif self._resultat_RMSE != 0: 
            return f"RMSE: {self._resultat_RMSE}"
        
        return "No s'ha calculat cap avaluacio"


        








