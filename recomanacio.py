

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
    """
    Classe abstracta que defineix l'estructura base d'un sistema de recomanació.
 
    Attributes:
        _recomanacio_final (dict): Diccionari amb els continguts recomanats i les seves puntuacions.
        _gestionador (Gestionador): Objecte que gestiona les dades del sistema.
        _usuari_a_comparar (int): Identificador de l'usuari per al qual es fa la recomanació.
    """

    _recomanacio_final: dict
    _gestionador: Gestionador
    _usuari_a_comparar: int

    def __init__(self,gestionador: Gestionador, usuari_a_comparar: int):
        """Inicialitza la recomanació amb el gestionador i l'usuari a comparar.
 
        Args:
            gestionador (Gestionador): Objecte que gestiona les dades del sistema.
            usuari_a_comparar (int): Identificador de l'usuari per al qual es fa la recomanació.
        """

        self._recomanacio_final = dict()
        self._gestionador = gestionador
        self._usuari_a_comparar = usuari_a_comparar
        logging.info(f"Recomanació inicialitzada")

    def get_recomanacio_final(self): 
        """Retorna el diccionari amb la recomanació final calculada.
 
        Returns:
            dict: Diccionari amb els continguts recomanats i les seves puntuacions.
        """
        return self._recomanacio_final

    @abstractmethod
    def trobar_similituds(self): 
        """Mètode abstracte per trobar similituds entre usuaris o continguts.
 
        Raises:
            NotImplementedError: Si la subclasse no implementa aquest mètode.
        """
        raise NotImplementedError

    @abstractmethod
    def calcular_recomanacio(self): 
        """Mètode abstracte per calcular la recomanació final.
 
        Raises:
            NotImplementedError: Si la subclasse no implementa aquest mètode.
        """
        raise NotImplementedError

    def __str__(self):
        """Retorna una representació en text de la recomanació final.
 
        Returns:
            str: Text formatat amb els títols, puntuacions i informació de cada contingut recomanat.
                 Retorna un missatge d'error si no s'han calculat recomanacions.
        """
        if self._recomanacio_final:
            logging.info(f"Recomanació final calculada i preparada per a visualització")
            resultat = str()
            if self._gestionador.get_tipus_contingut() == 'BOOKS':
                logging.info("Visualitzant recomanació per a BOOKS")

                for cont, score in self._recomanacio_final.items():
                    if cont not in self._gestionador.get_dict_contingut():  # ← afegeix això
                        continue
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
    """Recomanació simple basada en mitjanes globals i per contingut.
 
    Utilitza la fórmula de Bayesian Average per ponderar la puntuació de cada
    contingut combinant la seva mitjana individual amb la mitjana global.
 
    Attributes:
        _avg_general (float): Mitjana global de totes les valoracions del sistema.
        _avg_item (dict): Diccionari amb la mitjana de valoracions per a cada contingut.
        _num_vots (int): Nombre total de valoracions al sistema.
        _num_vots_item (dict): Diccionari amb el nombre de valoracions per a cada contingut.
    """

    _avg_general: float
    _avg_item: dict
    _num_vots: int
    _num_vots_item: dict

    def __init__(self, gestionador: Gestionador,usuari_a_comparar: int):
        """Inicialitza la recomanació simple amb valors per defecte.
 
        Args:
            gestionador (Gestionador): Objecte que gestiona les dades del sistema.
            usuari_a_comparar (int): Identificador de l'usuari per al qual es fa la recomanació.
        """

        super().__init__(gestionador,usuari_a_comparar)
        self._avg_general=0
        self._avg_item={}
        self._num_vots=0
        self._num_vots_item=dict() 

    def trobar_similituds(self):
        """Calcula les mitjanes globals i per contingut a partir de la matriu de dades.
 
        Recorre tota la matriu de valoracions per calcular la mitjana global del sistema
        i la mitjana individual de cada contingut, ignorant les valoracions amb valor 0.
        """

        dades = self._gestionador.get_matriu_dades()
        cont_index=self._gestionador.get_contingut_index()

        self._num_vots=np.count_nonzero(dades) 
    
        sumatori= dades.sum()
        self._avg_general= sumatori / self._num_vots if self._num_vots > 0 else 0.0

        for cont, columna in cont_index.items():
            valoracio=dades[:,columna]                                              #agafo tota la fila i una columna
            valoracions_reals=valoracio[valoracio>0]                                #agafo sol les valoracions que son diferents de 0

            # Si hi ha valoracions
            if valoracions_reals.size > 0:
                self._avg_item[cont] = valoracions_reals.mean()                    #mean calcula la mitjana de allo seleccionat
            else:
                self._avg_item[cont] = 0.0
            
            self._num_vots_item[cont] = valoracions_reals.size

        logging.info(f"Similituds trobades per a recomanació simple")
            
    def calcular_recomanacio(self, mode_avaluacio=False):
        """Calcula la puntuació final de cada contingut mitjançant Bayesian Average.
 
        Aplica la fórmula: score = (n/(n+m))*avg_item + (m/(n+m))*avg_general,
        on n és el nombre de vots del contingut i m és el mínim de vots requerit.
        Els continguts ja valorats per l'usuari s'exclouen tret que s'estigui en mode avaluació.
 
        Args:
            mode_avaluacio (bool): Si és True, inclou continguts ja valorats per l'usuari
                per permetre l'avaluació del sistema. Per defecte és False.
        """
    
        dades = self._gestionador.get_matriu_dades()
        fila_usuari = dades[self._gestionador.get_usuari_index()[self._usuari_a_comparar], :]

        dict_prov=dict()
        # Recorrem cada contingut i la seva mitjana
        for cont, avg in self._avg_item.items():

            columna = self._gestionador.get_contingut_index()[cont]
            
            if not mode_avaluacio and fila_usuari[columna] > 0:  # saltar perquè és usuari actual
                continue
            
            num_v_item = self._num_vots_item[cont]
            if num_v_item < MIN_VOTS:
                continue

            primera_part=((num_v_item/(num_v_item+MIN_VOTS))*avg)                       #si num_v_item es 0 pot donar 0 iau
            segona_part=((MIN_VOTS/(num_v_item+MIN_VOTS))*self._avg_general) 

            dict_prov[cont]=primera_part+segona_part

        sorted_dict = dict(sorted(dict_prov.items(), key=lambda item: item[1], reverse=True))
        
        if mode_avaluacio:
            #Filtrem només els que l'usuari ha vist
            vistos = {cont: score for cont, score in sorted_dict.items() 
              if fila_usuari[self._gestionador.get_contingut_index()[cont]] > 0}
            self._recomanacio_final = dict(list(vistos.items())[:NUM_RECOMANACIONS])
        else:
            self._recomanacio_final = dict(list(sorted_dict.items())[:NUM_RECOMANACIONS])
        logging.info(f"Recomanació calculada per a recomanació simple")

    def __str__(self):
        """Retorna una representació en text de la recomanació simple.
 
        Returns:
            str: Text formatat heretat de la classe base Recomanacio.
        """
        return super().__str__()



class RecomanacioColaborativa(Recomanacio):
    """Recomanació col·laborativa basada en similitud cosinus entre usuaris.
 
    Identifica els usuaris més similars a l'usuari objectiu i genera recomanacions
    ponderant les seves valoracions per la similitud respectiva.
 
    Attributes:
        _usuaris_similars (dict): Diccionari que mapeja cada ID d'usuari amb la seva
            similitud cosinus respecte a l'usuari a comparar.
    """

    _usuaris_similars: dict
    
    def __init__(self, gestionador: Gestionador,usuari_a_comparar: int):
        """Inicialitza la recomanació col·laborativa.
 
        Args:
            gestionador (Gestionador): Objecte que gestiona les dades del sistema.
            usuari_a_comparar (int): Identificador de l'usuari per al qual es fa la recomanació.
        """

        super().__init__(gestionador, usuari_a_comparar)
        self._usuaris_similars= dict()
        
    
    def trobar_similituds(self):
        """Calcula la similitud cosinus entre l'usuari objectiu i la resta d'usuaris.
 
        Només considera les valoracions en comú (on ambdós usuaris han puntuat
        el mateix contingut). Si no hi ha valoracions en comú, la similitud és 0.
        """
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


    def calcular_recomanacio(self, mode_avaluacio=False):
        """Calcula la similitud cosinus entre l'usuari objectiu i la resta d'usuaris.
 
        Només considera les valoracions en comú (on ambdós usuaris han puntuat
        el mateix contingut). Si no hi ha valoracions en comú, la similitud és 0.
        """
        dades = self._gestionador.get_matriu_dades()
        usuaris_index=self._gestionador.get_usuari_index()
        cont_index=self._gestionador.get_contingut_index()

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

        for cont, columna in cont_index.items():
            if not mode_avaluacio and fila_nou_usuari[columna] > 0:  
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
            
            self._recomanacio_final[cont]=total

        if mode_avaluacio:
            vistos = {cont: score for cont, score in self._recomanacio_final.items() if fila_nou_usuari[cont_index[cont]] > 0}
            self._recomanacio_final = dict(list(vistos.items())[:NUM_RECOMANACIONS])
        else:
            self._recomanacio_final = dict(list(sorted(self._recomanacio_final.items(), key=lambda x: x[1], reverse=True))[:NUM_RECOMANACIONS]) 

        logging.info(f"Recomanació calculada per a recomanació col·laborativa")
            
    def __str__(self):
        """Retorna una representació en text de la recomanació col·laborativa.
 
        Returns:
            str: Text formatat heretat de la classe base Recomanacio.
        """
        return super().__str__()
        
class RecomanacioBasadaContingut(Recomanacio):
    """Recomanació basada en contingut usant TF-IDF per calcular similituds entre gèneres.
 
    Construeix un perfil d'usuari a partir de les valoracions existents i els vectors
    TF-IDF dels gèneres de les pel·lícules, i utilitza la distància cosinus per
    recomanar els continguts més similars al perfil.
 
    Attributes:
        _matriu_generes (np.array): Matriu binària de gèneres per contingut (sense ponderar).
        _matriu_generes_ponderats (np.array): Matriu TF-IDF dels gèneres per contingut.
        _dict_similituts (dict): Diccionari amb les similituds cosinus calculades per contingut.
 
    Raises:
        NotImplementedError: Si s'intenta usar amb contingut de tipus BOOKS.
    """

    _matriu_generes: np.array
    _matriu_generes_ponderats: np.array
    _dict_similituts: dict

    def __init__(self,gestionador:Gestionador,usuari_a_comparar: int):
        """Inicialitza la recomanació basada en contingut.
 
        Args:
            gestionador (Gestionador): Objecte que gestiona les dades del sistema.
            usuari_a_comparar (int): Identificador de l'usuari per al qual es fa la recomanació.
        """

        super().__init__(gestionador,usuari_a_comparar)
        self._matriu_generes=np.array
        self._matriu_generes_ponderats=None
        self._dict_similituts=dict()
        

    def trobar_similituds(self):
        """Calcula la matriu TF-IDF dels gèneres de les pel·lícules.
 
        Transforma la llista de gèneres de cada pel·lícula en vectors TF-IDF
        per poder calcular posteriorment la similitud cosinus entre continguts.
 
        Raises:
            NotImplementedError: Si el tipus de contingut és BOOKS, ja que no
                disposa de dades de gèneres suficients per a aquest tipus.
        """

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


    
    def calcular_recomanacio(self, mode_avaluacio=False):
        """Calcula la recomanació final basada en el perfil d'usuari i la distància cosinus.
 
        Construeix el perfil d'usuari com la suma ponderada dels vectors TF-IDF
        dels continguts que ha valorat, normalitzada per la suma de valoracions.
        Després calcula la similitud cosinus entre el perfil i cada contingut.
 
        Args:
            mode_avaluacio (bool): Si és True, inclou continguts ja valorats per l'usuari
                per permetre l'avaluació del sistema. Per defecte és False.
 
        Raises:
            NotImplementedError: Si el tipus de contingut és BOOKS.
 
        Example:
            recomanacio = RecomanacioBasadaContingut(gestionador, 123)
            recomanacio.trobar_similituds()
            recomanacio.calcular_recomanacio()
            print(recomanacio)
        """

        if self._gestionador.get_tipus_contingut()=='BOOKS':
            raise NotImplementedError("No és possible fer recomanació basada en contingut amb books per falta de dades")
        
        dades=self._gestionador.get_matriu_dades()
        cont_index=self._gestionador.get_contingut_index()
        #perfil d'usuari
        perfil_usuari=np.zeros(self._matriu_generes_ponderats.shape[1])

        #puntuacions usuari
        puntuacions_usuari=dades[self._gestionador.get_usuari_index()[self._usuari_a_comparar],:]


        #multiplicacio i suma
        for movie, fila in cont_index.items():
            rating = puntuacions_usuari[fila]
            tfidf_movie = self._matriu_generes_ponderats[fila, :]
            perfil_usuari += rating * tfidf_movie

        perfil_usuari /= puntuacions_usuari.sum()

        #distancia cosinus i puntuacio final
        similitut_item=dict()
        usuari_p=sqrt(sum(punt**2 for punt in perfil_usuari))
        
        
        for movie,fila in cont_index.items():
            puntuacions_movies=self._matriu_generes_ponderats[fila, :]
            tfidf_p=sqrt(sum(punt**2 for punt in puntuacions_movies))
            
            sumatori=0
            for puntuacio1,puntuacio2 in zip(perfil_usuari,puntuacions_movies):
                sumatori+=puntuacio1*puntuacio2

            if usuari_p == 0 or tfidf_p == 0:

                similitut_item[movie] = 0.0
                continue

            if not mode_avaluacio and puntuacions_usuari[fila] > 0:  # ← aquí
                similitut_item[movie] = 0.0
                continue

            similitut_item[movie]=(sumatori/(usuari_p*tfidf_p))*PMAX
        
        sorted_sim = dict(sorted(similitut_item.items(), key=lambda x: x[1], reverse=True))

        if mode_avaluacio:
            vistos = {cont: score for cont, score in sorted_sim.items() if puntuacions_usuari[cont_index[cont]] > 0}
            self._recomanacio_final = dict(list(vistos.items())[:NUM_RECOMANACIONS])
        else:
            self._recomanacio_final = dict(list(sorted_sim.items())[:NUM_RECOMANACIONS])
        
        logging.info(f"Recomanació calculada per a recomanació basada en contingut")

    
    def __str__(self):
        """Retorna una representació en text de la recomanació basada en contingut.
 
        Returns:
            str: Text formatat heretat de la classe base Recomanacio.
        """
        return super().__str__()

    

