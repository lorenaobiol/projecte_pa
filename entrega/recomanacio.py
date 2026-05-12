from abc import ABC, abstractmethod 
from typing import List, Dict
import numpy as np
from entrega.gestionador import *
from entrega.contingut import Contingut
from entrega.usuari import Usuari
from entrega.config import *
from math import sqrt
import logging


#visualitzar!!
class Recomanacio(ABC):

    _recomanacio_final: dict
    _gestionador: Gestionador

    def __init__(self,gestionador: Gestionador):
        self._recomanacio_final = dict()
        self._gestionador = gestionador
    
    def get_recomanacio_final(self): return self._recomanacio_final
    @abstractmethod
    def trobar_similituds(self): return NotImplementedError
    @abstractmethod
    def calcular_recomanacio(self): return NotImplementedError
    @abstractmethod
    def __str__(self) -> str: return NotImplementedError




class RecomanacioSimple(Recomanacio):
    
    _avg_general: float
    _avg_item: dict
    _num_vots: int
    _num_vots_item: dict


    def __init__(self,gestionador: Gestionador):
        super().__init__(gestionador)
    
        self._avg_general=0
        self._avg_item={}
        self._num_vots=0
        self._num_vots_item=dict() #acabar
     

    def trobar_similituds(self, iduser:int): 
        dades = self._gestionador.get_matriu_dades()
        movie_index=self._gestionador.get_contingut_index()

        self._num_vots=np.count_nonzero(dades) #conto els vots que son 0?
    
        sumatori= dades.sum()
        self._avg_general= sumatori / self._num_vots if self._num_vots > 0 else 0.0

        for movie, columna in movie_index.items():
            valoracio=dades[:,columna]                                              #agafo tota la fila i una columna
            valoracions_reals=valoracio[valoracio>0]                                 #agafo sol les valoracions que son diferents de 0

            if valoracions_reals.size > 0:
                self._avg_item[movie] = valoracions_reals.mean()                    #mean calcula la mitjana de allo seleccionat
            else:
                self._avg_item[movie] = 0.0
            
            self._num_vots_item[movie] = valoracions_reals.size
            
    def calcular_recomanacio(self):

        for movie, avg in self._avg_item.items():
            num_v_item = self._num_vots_item[movie]

            if num_v_item < MIN_VOTS:
                continue

            primera_part=((num_v_item/(num_v_item+MIN_VOTS))*avg)                       #si num_v_item es 0 pot donar 0 iau
            segona_part=((MIN_VOTS/(num_v_item+MIN_VOTS))*self._avg_general) 

            self._recomanacio_final[movie]=primera_part+segona_part

    def __str__(self):

        resultat = str()
        for llibre, score in sorted(self._recomanacio_final.items(),key=lambda x: x[1],reverse=True):
            resultat += f"{llibre}: {score:.2f}\n"
        return resultat


class RecomanacioColaborativa(Recomanacio):

    _usuaris_similars: dict
    _usuari_a_comparar: int

    def __init__(self,gestionador:Gestionador):
        '''Inicialitza la classe RecomanacioColaborativa_Movie amb un gestionador de dades.'''
        super().__init__(gestionador)
        self._usuaris_similars= dict()
        self._usuari_a_comparar=0
    
    def trobar_similituds(self, userID:int):
        dades = self._gestionador.get_matriu_dades() 
        usuaris_index=self._gestionador.get_usuari_index()

        similituds=dict()
        
        fila_usuari_actual=usuaris_index[userID]
        valoracions_u_act=dades[fila_usuari_actual,:]

        
        for IDuser,fila in usuaris_index.items():

            if IDuser == userID:                                        # No cal comparar l'usuari amb ell mateix
                self._usuari_a_comparar = userID
                continue

            valoracions=dades[fila,:]
            en_comu = (valoracions_u_act > 0) & (valoracions > 0)       #Aixo crea un filtre de TRUE o  FALSE | si se compleix a les 2 es true


            val_1=valoracions_u_act[en_comu]
            val_2=valoracions[en_comu]

            if len(val_1) == 0:
                similituds[IDuser] = 0.0
                continue

            numerador = np.sum(val_1 * val_2)
            denominador = np.sqrt(np.sum(val_1**2)) * np.sqrt(np.sum(val_2**2))

            similituds[IDuser] = 0.0 if denominador == 0 else numerador / denominador
        
        self._usuaris_similars= similituds

    def calcular_recomanacio(self):
        dades = self._gestionador.get_matriu_dades()
        usuaris_index=self._gestionador.get_usuari_index()
        movies_index=self._gestionador.get_contingut_index()

        dict_similituds=dict()

        #Amb una funcio lambda:
        de_gran_a_petit=sorted(self._usuaris_similars.items(), key=lambda x: x[1], reverse=True)

        for x in range(NUM_RECOMANACIONS):
            IDuser, similitud = de_gran_a_petit[x]
            dict_similituds[IDuser] = [similitud]

        for IDuser,fila in usuaris_index.items():
            if IDuser in dict_similituds.keys():

                fila_real=dades[fila,:]
                notes=fila_real[fila_real>0]

                if len(notes) > 0:
                    mitjana_usuari = notes.mean()
                else:
                    mitjana_usuari = 0.0

                dict_similituds[IDuser].append(mitjana_usuari)

        #Calcul de la mitjana individual del usuari a comparar.
        llista_user=dades[usuaris_index[self._usuari_a_comparar],:]
        mitjana_user=llista_user[llista_user>0].mean() if len(llista_user[llista_user>0])>0 else 0.0

        #Calcul del total de les similituts
        
        total_similituts=sum([s[0] for s in dict_similituds.values()])  #logging
        if total_similituts == 0:
            return

        #Fila per saber si ja ha vist la pelicula o no.
        fila_nou_usuari = dades[usuaris_index[self._usuari_a_comparar], :]

        for movie, columna in movies_index.items():
            if fila_nou_usuari[columna] > 0:  
                continue
            sumatori=0
            for user, fila in usuaris_index.items():
                if user in dict_similituds:
                    nota=dades[fila,columna]
                    if nota>0:
                        similitut=dict_similituds[user][0]
                        mitjana=dict_similituds[user][1]

                        sumatori+=similitut*(nota-mitjana)
            divisio=sumatori/total_similituts

            total=mitjana_user+divisio
            
            self._recomanacio_final[movie]=total 

            #on esta pinckle
            #com executem el fitxer
        
class RecomanacioBasadaContingut(Recomanacio):

    def __init__(self,gestionador:Gestionador):
        super().__init__(gestionador)
        self._matriu_generes=np.array
        self._matriu_generes_ponderats=np.array
        self._dict_similituts=dict()

    def trobar_similituds(self, iduser:int):

        if self._gestionador.get_tipus_contingut()=='BOOKS':
            raise NotImplementedError("No és possible fer recomanació basada en contingut amb books per falta de dades")

        dades_movies=self._gestionador.get_dict_contingut()

        








    def calcular_recomanacio(self):
        
        if self._gestionador.get_tipus_contingut()=='BOOKS':
            raise NotImplementedError("No és possible fer recomanació basada en contingut amb books per falta de dades")


    






                


                





            


            


        

        


