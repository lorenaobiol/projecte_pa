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
from math import sqrt
from sklearn.feature_extraction.text import TfidfVectorizer

from entrega.gestionador import *
from entrega.contingut import Contingut
from entrega.usuari import Usuari
from entrega.config import *


class Recomanacio(ABC):
    """
    Classe abstracta base per totes les recomanacions.

    Attributes:
        _recomanacio_final (dict):
            Diccionari amb el resultat final de la recomanació.

        _gestionador (Gestionador):
            Objecte encarregat de gestionar les dades.
    """

    _recomanacio_final: dict
    _gestionador: Gestionador

    def __init__(self, gestionador: Gestionador):
        """
        Inicialitza la recomanació.

        Args:
            gestionador (Gestionador):
                Gestionador amb les dades del sistema.
        """

        # Diccionari on es guardaran
        # les puntuacions finals
        self._recomanacio_final = dict()

        # Objecte que gestiona totes les dades
        self._gestionador = gestionador

    def get_recomanacio_final(self):
        """
        Retorna la recomanació final.

        Returns:
            dict:
                Diccionari amb les puntuacions finals.
        """

        return self._recomanacio_final

    @abstractmethod
    def trobar_similituds(self):
        """
        Calcula les similituds necessàries per la recomanació.
        """

        raise NotImplementedError

    @abstractmethod
    def calcular_recomanacio(self):
        """
        Calcula la recomanació final.
        """

        raise NotImplementedError

    def __str__(self):
        """
        Retorna un string amb les recomanacions calculades.

        Returns:
            str:
                Text formatat amb les puntuacions.
        """

        #mostrar el nom de la peli o llibre i la puntuacio.
        #llibre: isbn, titul, autor, any, editorial
        #movies: id , titul i generes

        # Si ja s'han calculat recomanacions
        if self._recomanacio_final:

            resultat = (
                "Llista de les puntuacions "
                "de la Recomanació\n"
            )
            #!!!!!!!! if llibre o movie:
            # Recorrem totes les recomanacions
            for cont, score in self._recomanacio_final.items():

                # Afegim cada contingut amb la seva puntuació
                resultat += f"{cont}: {score:.2f}\n"

            return resultat

        # Missatge si encara no hi ha càlculs
        return "No s'ha calculat cap recomanació encara."


class RecomanacioSimple(Recomanacio):
    """
    Recomanació basada en la mitjana de puntuacions.
    """

    _avg_general: float
    _avg_item: dict
    _num_vots: int
    _num_vots_item: dict

    def __init__(self, gestionador: Gestionador):
        """
        Inicialitza la recomanació simple.

        Args:
            gestionador (Gestionador):
                Gestionador de dades.
        """

        super().__init__(gestionador)

        # Mitjana global de totes les valoracions
        self._avg_general = 0

        # Diccionari amb la mitjana de cada contingut
        self._avg_item = {}

        # Número total de valoracions
        self._num_vots = 0

        # Número de vots de cada contingut
        self._num_vots_item = dict()  #acabar

    def trobar_similituds(self, iduser: int):
        """
        Calcula les mitjanes globals i per contingut.

        Args:
            iduser (int):
                ID de l'usuari.
        """

        # Matriu de valoracions
        dades = self._gestionador.get_matriu_dades()

        # Diccionari contingut -> columna
        movie_index = self._gestionador.get_contingut_index()

        # Comptem totes les valoracions diferents de 0
        self._num_vots = np.count_nonzero(dades)

        # Suma total de totes les valoracions
        sumatori = dades.sum()

        # Mitjana global del sistema
        self._avg_general = (
            sumatori / self._num_vots
            if self._num_vots > 0
            else 0.0
        )

        # Recorrem cada contingut
        for movie, columna in movie_index.items():

            # Agafo totes les files d'una columna
            valoracio = dades[:, columna]  #agafo tota la fila i una columna

            # Filtrar només valoracions > 0
            valoracions_reals = (
                valoracio[valoracio > 0]
            )  #agafo sol les valoracions diferents de 0

            # Si hi ha valoracions
            if valoracions_reals.size > 0:

                # Calcular mitjana del contingut
                self._avg_item[movie] = (
                    valoracions_reals.mean()
                )  #mean calcula la mitjana

            else:
                self._avg_item[movie] = 0.0

            # Guardem número de valoracions
            self._num_vots_item[movie] = (
                valoracions_reals.size
            )

    def calcular_recomanacio(self):
        """
        Calcula la puntuació final de cada contingut.
        """

        #falta el nou usuari


        # Recorrem cada contingut i la seva mitjana
        for movie, avg in self._avg_item.items():

            # Número de vots del contingut
            num_v_item = self._num_vots_item[movie]

            # Si no arriba al mínim de vots
            if num_v_item < MIN_VOTS:
                continue

            primera_part = (
                (num_v_item / (num_v_item + MIN_VOTS))
                * avg
            )  #si num_v_item es 0 dona 0

            segona_part = (
                (MIN_VOTS / (num_v_item + MIN_VOTS))
                * self._avg_general
            )

            # Fórmula de recomanació ponderada
            self._recomanacio_final[movie] = (
                primera_part + segona_part
            )

    def __str__(self):
        """
        Retorna la recomanació en format string.
        """

        return super().__str__()


class RecomanacioColaborativa(Recomanacio):
    """
    Recomanació col·laborativa basada en similitud entre usuaris.
    """

    _usuaris_similars: dict
    _usuari_a_comparar: int

    def __init__(self, gestionador: Gestionador):
        """
        Inicialitza la recomanació col·laborativa.

        Args:
            gestionador (Gestionador):
                Gestionador de dades.
        """

        super().__init__(gestionador)

        # Diccionari amb similituds entre usuaris
        self._usuaris_similars = dict()

        # Usuari pel qual es faran recomanacions
        self._usuari_a_comparar = 0

    def trobar_similituds(self, userID: int):
        """
        Calcula la similitud entre usuaris.

        Args:
            userID (int):
                Usuari del qual es volen recomanacions.
        """

        dades = self._gestionador.get_matriu_dades()

        usuaris_index = (
            self._gestionador.get_usuari_index()
        )

        # Diccionari on guardarem similituds
        similituds = dict()

        # Fila de l'usuari actual
        fila_usuari_actual = usuaris_index[userID]

        # Valoracions de l'usuari actual
        valoracions_u_act = dades[fila_usuari_actual, :]

        # Recorrem tots els usuaris
        for IDuser, fila in usuaris_index.items():

            # No comparem amb ell mateix
            if IDuser == userID:
                # No cal comparar l'usuari amb ell mateix
                self._usuari_a_comparar = userID
                continue

            # Valoracions del segon usuari
            valoracions = dades[fila, :]

            # Continguts puntuats pels dos usuaris
            en_comu = (
                (valoracions_u_act > 0)
                & (valoracions > 0)
            )  #filtre de TRUE o FALSE

            val_1 = valoracions_u_act[en_comu]
            val_2 = valoracions[en_comu]

            # Si no tenen continguts en comú
            if len(val_1) == 0:
                similituds[IDuser] = 0.0
                continue

            # Producte escalar
            numerador = np.sum(val_1 * val_2)

            # Mòduls dels vectors
            denominador = (
                np.sqrt(np.sum(val_1 ** 2))
                * np.sqrt(np.sum(val_2 ** 2))
            )

            # Similitud cosinus
            similituds[IDuser] = (
                0.0
                if denominador == 0
                else numerador / denominador
            )

        self._usuaris_similars = similituds


    def calcular_recomanacio(self):
        """
        Calcula les recomanacions col·laboratives.
        """

        dades = self._gestionador.get_matriu_dades()

        usuaris_index = (
            self._gestionador.get_usuari_index()
        )

        movies_index = (
            self._gestionador.get_contingut_index()
        )

        # Diccionari amb usuaris més similars
        dict_similituds = dict()

        # Ordenar usuaris de més similar a menys
        #Amb una funcio lambda:
        de_gran_a_petit = sorted(
            self._usuaris_similars.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Seleccionem els N millors usuaris
        for x in range(NUM_RECOMANACIONS):

            IDuser, similitud = de_gran_a_petit[x]

            dict_similituds[IDuser] = [similitud]

        # Calcular la mitjana de cada usuari similar
        for IDuser, fila in usuaris_index.items():

            if IDuser in dict_similituds.keys():

                fila_real = dades[fila, :]

                notes = fila_real[fila_real > 0]

                if len(notes) > 0:
                    mitjana_usuari = notes.mean()

                else:
                    mitjana_usuari = 0.0

                dict_similituds[IDuser].append(
                    mitjana_usuari
                )

        #Calcul de la mitjana individual del usuari
        llista_user = dades[
            usuaris_index[self._usuari_a_comparar], :
        ]

        mitjana_user = (
            llista_user[llista_user > 0].mean()
            if len(llista_user[llista_user > 0]) > 0
            else 0.0
        )

        #Calcul del total de les similituds
        total_similituts = sum(
            [s[0] for s in dict_similituds.values()]
        )

        # Evitar divisió entre 0
        if total_similituts == 0:
            return

        #Fila per saber si ja ha vist la pelicula o no
        fila_nou_usuari = dades[
            usuaris_index[self._usuari_a_comparar], :
        ]

        # Recorrem cada contingut
        for movie, columna in movies_index.items():

            # Si l'usuari ja l'ha valorat
            if fila_nou_usuari[columna] > 0:
                continue

            sumatori = 0

            # Recorrem usuaris similars
            for user, fila in usuaris_index.items():

                if user in dict_similituds:

                    nota = dades[fila, columna]

                    # Si l'usuari ha valorat el contingut
                    if nota > 0:

                        similitut = (
                            dict_similituds[user][0]
                        )

                        mitjana = (
                            dict_similituds[user][1]
                        )

                        # Fórmula ponderada
                        sumatori += (
                            similitut * (nota - mitjana)
                        )

            divisio = sumatori / total_similituts

            total = mitjana_user + divisio

            # Guardem recomanació final
            self._recomanacio_final[movie] = total

        return self._recomanacio_final

        #on esta pickle
        #com executem el fitxer

    def __str__(self):
        """
        Retorna la recomanació en format string.
        """

        return super().__str__()


class RecomanacioBasadaContingut(Recomanacio):
    """
    Recomanació basada en les característiques del contingut.
    """

    def __init__(self, gestionador: Gestionador):
        """
        Inicialitza la recomanació basada en contingut.

        Args:
            gestionador (Gestionador):
                Gestionador de dades.
        """

        super().__init__(gestionador)

        # Matriu de característiques dels continguts
        self._matriu_generes = np.array

        # Matriu TF-IDF ponderada
        self._matriu_generes_ponderats = None

        # Diccionari amb similituds
        self._dict_similituts = dict()

        # Usuari a recomanar
        self._usuari: int = None

    def trobar_similituds(self, iduser: int):
        """
        Genera la matriu TF-IDF dels gèneres.

        Args:
            iduser (int):
                Usuari a analitzar.
        """

        # No disponible per BOOKS
        if self._gestionador.get_tipus_contingut() == 'BOOKS':

            raise NotImplementedError(
                "No és possible fer recomanació "
                "basada en contingut amb books "
                "per falta de dades"
            )

        dades_movies = (
            self._gestionador.get_dict_contingut()
        )

        movies_index = (
            self._gestionador.get_contingut_index()
        )

        #representacio tf-idf
        item_features = [
            ' '.join(
                dades_movies[movie].get_generes()
            )
            for movie in movies_index
        ]

        # Crear model TF-IDF
        tfidf = TfidfVectorizer(
            stop_words='english'
        )

        # Transformar gèneres a vectors numèrics
        tfidf_matrix = (
            tfidf.fit_transform(item_features)
            .toarray()
        )

        # Guardar matriu
        self._matriu_generes_ponderats = tfidf_matrix

        # Guardar usuari actual
        self._usuari = iduser

    def calcular_recomanacio(self):
        """
        Calcula recomanacions basades en contingut.
        """

        dades = self._gestionador.get_matriu_dades()

        movies_index = (
            self._gestionador.get_contingut_index()
        )

        #perfil d'usuari
        perfil_usuari = np.zeros(
            self._matriu_generes_ponderats.shape[1]
        )

        #puntuacions usuari
        puntuacions_usuari = dades[
            self._gestionador.get_usuari_index()[
                self._usuari
            ],
            :
        ]

        #multiplicacio i suma
        for movie, fila in movies_index.items():

            # Nota que ha posat l'usuari
            rating = puntuacions_usuari[fila]

            # Vector TF-IDF del contingut
            tfidf_movie = (
                self._matriu_generes_ponderats[fila, :]
            )

            # Construcció del perfil de l'usuari
            perfil_usuari += (
                rating * tfidf_movie
            )

        # Normalitzar perfil
        perfil_usuari /= puntuacions_usuari.sum()

        #distancia cosinus i puntuacio final
        similitut_item = dict()

        # Mòdul del perfil de l'usuari
        usuari_p = sqrt(
            sum(
                punt ** 2
                for punt in perfil_usuari
            )
        )

        # Recorrem tots els continguts
        for movie, fila in movies_index.items():

            puntuacions_movies = (
                self._matriu_generes_ponderats[fila, :]
            )

            # Mòdul del vector TF-IDF
            tfidf_p = sqrt(
                sum(
                    punt ** 2
                    for punt in puntuacions_movies
                )
            )

            sumatori = 0

            # Producte escalar entre vectors
            for puntuacio1, puntuacio2 in zip(
                perfil_usuari,
                puntuacions_movies
            ):

                sumatori += (
                    puntuacio1 * puntuacio2
                )

            # Evitar divisió entre 0
            if usuari_p == 0 or tfidf_p == 0:

                similitut_item[movie] = 0.0
                continue

            # Similitud cosinus escalada
            similitut_item[movie] = (
                (sumatori / (usuari_p * tfidf_p))
                * PMAX
            )

        # Guardar recomanacions finals
        self._recomanacio_final = similitut_item

        return self._recomanacio_final

    def __str__(self):
        """
        Retorna la recomanació en format string.
        """

        return super().__str__()