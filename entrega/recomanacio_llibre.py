import csv
from abc import ABC, abstractmethod 
from typing import List, Dict
from entrega.gestionador import Gestionador
from entrega.contingut import Contingut
from entrega.usuari import Usuari
from entrega.config import *

class Recomanacio_Llibre(ABC):

    _recomanacio_final: List
    _gestionador: Gestionador

    def __init__(self,gestionador: Gestionador):
        self._recomanacio_final = []
        self._gestionador = gestionador
    
    def get_recomanacio_final(self):    
        return self._recomanacio_final
    
    @abstractmethod
    def trobar_similituds(self):
        return NotImplementedError

    @abstractmethod
    def calcular_recomanacio(self):
        return NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        return NotImplementedError




class RecomanacioSimple(Recomanacio_Llibre):
    _avg_general: float
    _avg_item: dict
    _num_vots: int


    def __init__(self,gestionador: Gestionador):
        super().__init__(gestionador)
        self._dict_contingut: dict = {}
        self._avg_general=0
        self._avg_item={}
        self._num_vots=0
     

    def trobar_similituds(self, usuari:Usuari): #importa si al int que entro li canvio el nom?
        dades = self._gestionador.get_matriu_dades()

        #calcul avg_general i avg_item i num_vots
        sumatori_total=0
        valoracions_total=0
        for userID, contingut in dades.items():
            sumatori_item=0
            valoracions_item=0
            for contID, valoracio in contingut.items():
                if valoracio !=0:
                    sumatori_total+=valoracio
                    sumatori_item+=valoracio
                    valoracions_total+=1 #aixo funciona?
                    valoracions_item+=1
            
            self._avg_item[contID] = sumatori_item/valoracions_item
        
        self._avg_general=sumatori_total/valoracions_total
        self._num_vots=valoracions_total
        
        
    def calcular_recomanacio(self):
        primera_part=((self._num_vots/(self._num_vots+MIN_VOTS))*self._avg_item)
        segona_part=((self._min_vots/(self._num_vots+self._min_vots))*self._avg_general)

        self._recomanacio_final=primera_part+segona_part

    def __str__(self):
        #???? titol
        return '\n'.join([str(x) for x in self._recomanacio_final])


class RecomanacioColaborativa(Recomanacio_Llibre):

    _usuaris_similars:List

    def __init__(self,gestionador:Gestionador):
        super().__init__(gestionador)
        self._usuaris_similars: List = []
    
    def trobar_similituds(self,k:int, userID:int):
        dades = self._gestionador.get_matriu_dades() #mirar de ficar un super 
        usuari_actual=None
        for IDuser,contingut in dades.items():
            if userID == IDuser:
                usuari_actual=contingut
        sumatori=0
        arrel1=0
        arrel2=0
        for IDuse,content in dades.items():


recomanacio_basat_contingut
- no va ficar li print etc
-no implementat per falta de dades