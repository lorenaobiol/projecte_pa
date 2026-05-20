#canviar tots los movies per contingut(mes general)
#visualitzar!!

"""
Mòdul de recomanacions.

Aquest fitxer conté les diferents estratègies de recomanació:
- Recomanació simple
- Recomanació col·laborativa
- Recomanació basada en contingut
"""

from abc import ABC, abstractmethod
from typing import Dict
import numpy as np
from gestionador import *
from contingut import Contingut
from usuari import Usuari
from config import *
from math import sqrt
import logging
from sklearn.feature_extraction.text import TfidfVectorizer

logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)

class Recomanacio(ABC):

    _recomanacio_final: dict
    _gestionador: Gestionador
    _usuari_a_comparar: int

    def __init__(self,gestionador: Gestionador, usuari_a_comparar: int):
        self._recomanacio_final = dict()
        self._gestionador = gestionador
        self._usuari_a_comparar = usuari_a_comparar
        logging.info(f"Recomanació inicialitzada")

    def get_recomanacio_final(self): return self._recomanacio_final

    @abstractmethod
    def trobar_similituds(self): raise NotImplementedError

    @abstractmethod
    def calcular_recomanacio(self): raise NotImplementedError

    def __str__(self):

        if self._recomanacio_final:
            logging.info(f"Recomanació final calculada i preparada per a visualització")
            resultat = str()
            if self._gestionador.get_tipus_contingut() == 'BOOKS':
                logging.info("Visualitzant recomanació per a BOOKS")

                for cont, score in self._recomanacio_final.items():
                    info = self._gestionador.get_dict_contingut()[cont]
                    titol=info.get_titol()
                    codi=info.get_isbn()
                    autor=info.get_autor()
                    any=info.get_any()
                    resultat += f"{titol}\nPuntuació:{score:.2f}\nInformació del llibre: (ISBN: {codi}, Autor: {autor}, Any: {any})\n\n"
    
            elif self._gestionador.get_tipus_contingut() == 'MOVIES':
                logging.info("Visualitzant recomanació per a MOVIES")
                
                for cont, score in self._recomanacio_final.items():
                    info = self._gestionador.get_dict_contingut()[cont]
                    titol=info.get_titol()
                    generes=', '.join(info.get_generes())
                    resultat += f"{titol}\nPuntuació:{score:.2f}\nInformació de la pel·lícula: (Codi: {cont}, Gèneres: {generes})\n\n"

            else:
                logging.warning(f"Recomanació no calculada")
                return "No s'han calculat recomanacions"

            print('Resultats:')
            logging.info(f"Recomanació visualitzada per a l'usuari {self._usuari_a_comparar}")
            return resultat


class RecomanacioSimple(Recomanacio):
    ''''''

    _avg_general: float
    _avg_item: dict
    _num_vots: int
    _num_vots_item: dict

    def __init__(self, gestionador: Gestionador,usuari_a_comparar: int):
        super().__init__(gestionador,usuari_a_comparar)
    
        self._avg_general=0
        self._avg_item={}
        self._num_vots=0
        self._num_vots_item=dict() 

    def trobar_similituds(self):
        """
        Calcula les mitjanes globals i per contingut.

        Args:
            iduser (int):
                ID de l'usuari.
        """

        dades = self._gestionador.get_matriu_dades()
        movie_index=self._gestionador.get_contingut_index()

        self._num_vots=np.count_nonzero(dades) 
    
        sumatori= dades.sum()
        self._avg_general= sumatori / self._num_vots if self._num_vots > 0 else 0.0

        for movie, columna in movie_index.items():
            valoracio=dades[:,columna]                                              #agafo tota la fila i una columna
            valoracions_reals=valoracio[valoracio>0]                                #agafo sol les valoracions que son diferents de 0

            # Si hi ha valoracions
            if valoracions_reals.size > 0:
                self._avg_item[movie] = valoracions_reals.mean()                    #mean calcula la mitjana de allo seleccionat
            else:
                self._avg_item[movie] = 0.0
            
            self._num_vots_item[movie] = valoracions_reals.size

            logging.info(f"Similituds trobades per a recomanació simple")
            
    def calcular_recomanacio(self):
        """
        Calcula la puntuació final de cada contingut.
        """

        #falta el nou usuari!!!!!!
        dades = self._gestionador.get_matriu_dades()
        fila_usuari = dades[self._gestionador.get_usuari_index()[self._usuari_a_comparar], :]


        # Recorrem cada contingut i la seva mitjana
        for movie, avg in self._avg_item.items():

            columna = self._gestionador.get_contingut_index()[movie]
            
            if fila_usuari[columna] > 0:  # saltar perquè és usuari actual
                continue
            
            num_v_item = self._num_vots_item[movie]
            if num_v_item < MIN_VOTS:
                continue

            primera_part=((num_v_item/(num_v_item+MIN_VOTS))*avg)                       #si num_v_item es 0 pot donar 0 iau
            segona_part=((MIN_VOTS/(num_v_item+MIN_VOTS))*self._avg_general) 

            self._recomanacio_final[movie]=primera_part+segona_part

            logging.info(f"Recomanació calculada per a recomanació simple")

    def __str__(self):
        return super().__str__()



class RecomanacioColaborativa(Recomanacio):

    _usuaris_similars: dict
    

    def __init__(self, gestionador: Gestionador,usuari_a_comparar: int):

        super().__init__(gestionador, usuari_a_comparar)
        self._usuaris_similars= dict()
        
    
    def trobar_similituds(self):
        dades = self._gestionador.get_matriu_dades() 
        usuaris_index=self._gestionador.get_usuari_index()

        similituds=dict()
        
        fila_usuari_actual=usuaris_index[self._usuari_a_comparar]
        valoracions_u_act=dades[fila_usuari_actual,:]

        
        for IDuser,fila in usuaris_index.items():

            if IDuser == self._usuari_a_comparar:                                        # No cal comparar l'usuari amb ell mateix
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

        logging.info(f"Similituds trobades per a recomanació col·laborativa")


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

        #Fila per sawhereber si ja ha vist la pelicula o no.
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

            logging.info(f"Recomanació calculada per a recomanació col·laborativa")
            
    def __str__(self):
        super().__str__()
        
class RecomanacioBasadaContingut(Recomanacio):

    def __init__(self,gestionador:Gestionador,usuari_a_comparar: int):
        super().__init__(gestionador,usuari_a_comparar)
        self._matriu_generes=np.array
        self._matriu_generes_ponderats=None
        self._dict_similituts=dict()
        

    def trobar_similituds(self):

        if self._gestionador.get_tipus_contingut()=='BOOKS':
            raise NotImplementedError("No és possible fer recomanació basada en contingut amb books per falta de dades")

        dades_movies=self._gestionador.get_dict_contingut()
        movies_index=self._gestionador.get_contingut_index()
        

        #representacio tf-idf
        item_features = [' '.join(dades_movies[movie].get_generes()) for movie in movies_index]
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(item_features).toarray()
        self._matriu_generes_ponderats=tfidf_matrix

        logging.info(f"Similituds trobades per a recomanació basada en contingut")


    
    def calcular_recomanacio(self ):
        #ficar lo q ve ara a calcular recomanacio.
        dades=self._gestionador.get_matriu_dades()
        movies_index=self._gestionador.get_contingut_index()
        #perfil d'usuari
        perfil_usuari=np.zeros(self._matriu_generes_ponderats.shape[1])

        #puntuacions usuari

        puntuacions_usuari=dades[self._gestionador.get_usuari_index()[self._usuari_a_comparar],:]


        #multiplicacio i suma
        for movie, fila in movies_index.items():
            rating = puntuacions_usuari[fila]
            tfidf_movie = self._matriu_generes_ponderats[fila, :]
            perfil_usuari += rating * tfidf_movie

        perfil_usuari /= puntuacions_usuari.sum()

        #distancia cosinus i puntuacio final
        similitut_item=dict()
        usuari_p=sqrt(sum(punt**2 for punt in perfil_usuari))
        
        
        for movie,fila in movies_index.items():
            puntuacions_movies=self._matriu_generes_ponderats[fila, :]
            tfidf_p=sqrt(sum(punt**2 for punt in puntuacions_movies))
            
            sumatori=0
            for puntuacio1,puntuacio2 in zip(perfil_usuari,puntuacions_movies):
                sumatori+=puntuacio1*puntuacio2

            if usuari_p == 0 or tfidf_p == 0:

                similitut_item[movie] = 0.0
                continue

            similitut_item[movie]=(sumatori/(usuari_p*tfidf_p))*PMAX
        
        self._recomanacio_final=similitut_item
        logging.info(f"Recomanació calculada per a recomanació basada en contingut")

    
    def __str__(self):
        super().__str__()

        
        

            























    def calcular_recomanacio(self):
        
        if self._gestionador.get_tipus_contingut()=='BOOKS':
            raise NotImplementedError("No és possible fer recomanació basada en contingut amb books per falta de dades")


    






                


                





            


            


        

        


