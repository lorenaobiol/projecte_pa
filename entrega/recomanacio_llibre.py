from abc import ABC, abstractmethod
from typing import Dict
import numpy as np

from entrega.gestionador import Gestionador
from entrega.usuari import Usuari
from entrega.config import *


class Recomanacio_Llibre(ABC):

    _recomanacio_final: dict
    _gestionador: Gestionador

    def __init__(self, gestionador: Gestionador):
        self._recomanacio_final = dict()
        self._gestionador = gestionador

    def get_recomanacio_final(self):
        return self._recomanacio_final

    @abstractmethod
    def trobar_similituds(self):
        pass

    @abstractmethod
    def calcular_recomanacio(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class RecomanacioSimple(Recomanacio_Llibre):

    _avg_general: float
    _avg_item: dict
    _num_vots: int
    _num_vots_item: dict

    def __init__(self, gestionador: Gestionador):
        super().__init__(gestionador)

        self._avg_general = 0
        self._avg_item = {}
        self._num_vots = 0
        self._num_vots_item = {}

    
    def trobar_similituds(self, usuari: Usuari):

        dades = self._gestionador.get_matriu_dades()
        #aixo es l'unic q canvia (nom d variable)
        book_index = self._gestionador.get_contingut_index()

        self._num_vots = np.count_nonzero(dades)

        sumatori = dades.sum()

        # FER-HO TMB A MOVIES SI NO POT PETAR
        if self._num_vots > 0:
            self._avg_general = sumatori / self._num_vots
        else:
            self._avg_general = 0.0

        # calcular avg de cada llibre
        for llibre, columna in book_index.items():
            valoracions = dades[:, columna]
            valoracions_reals = valoracions[valoracions > 0]
            if valoracions_reals.size > 0:
                self._avg_item[llibre] = valoracions_reals.mean()
            else:
                self._avg_item[llibre] = 0.0

            self._num_vots_item[llibre] = valoracions_reals.size

    def calcular_recomanacio(self):

        for llibre, avg in self._avg_item.items():

            num_v_item = self._num_vots_item[llibre]

            # MIRAR SI HO POSEM: descartar items amb pocs vots
            if num_v_item < MIN_VOTS:
                continue

            primera_part = ((num_v_item / (num_v_item + MIN_VOTS)) * avg)
            segona_part = ((MIN_VOTS / (num_v_item + MIN_VOTS)) * self._avg_general)
            score = primera_part + segona_part
            self._recomanacio_final[llibre] = score

    def __str__(self):

        resultat = ""

        for llibre, score in sorted(self._recomanacio_final.items(),key=lambda x: x[1],reverse=True):
            resultat += f"{llibre}: {score:.2f}\n"
        return resultat


class RecomanacioColaborativa(Recomanacio_Llibre):

    _usuaris_similars: dict
    _usuari_a_comparar: int

    def __init__(self, gestionador: Gestionador_BOOKS):

        super().__init__(gestionador)

        self._usuaris_similars = dict()
        self._usuari_a_comparar = 0

    def trobar_similituds(self, userID: int):

        dades = self._gestionador.get_matriu_dades()
        usuaris_index = self._gestionador.get_usuari_index()

        similituds = dict()

        fila_usuari_actual = usuaris_index[userID]

        valoracions_u_act = dades[fila_usuari_actual, :]

        for IDuser, fila in usuaris_index.items():

            if IDuser == userID:

                self._usuari_a_comparar = userID
                continue

            valoracions = dades[fila, :]

            en_comu = ((valoracions_u_act > 0)&(valoracions > 0))

            val_1 = valoracions_u_act[en_comu]
            val_2 = valoracions[en_comu]

            if len(val_1) == 0:
                similituds[IDuser] = 0.0
                continue

            numerador = np.sum(val_1 * val_2)

            denominador = (np.sqrt(np.sum(val_1 ** 2))*np.sqrt(np.sum(val_2 ** 2)))
            
            #POSAR TMB A MOVIES
            if denominador == 0:
                similituds[IDuser] = 0.0
            else:
                similituds[IDuser] = numerador / denominador
            
        self._usuaris_similars = similituds

    def calcular_recomanacio(self):

        dades = self._gestionador.get_matriu_dades()

        usuaris_index = self._gestionador.get_usuari_index()

        books_index = self._gestionador.get_contingut_index()

        dict_similituds = dict()

        de_gran_a_petit = sorted(self._usuaris_similars.items(),key=lambda x: x[1],reverse=True)

        #NS SI POSAR_HO (ES PER Puede petar si hay menos usuarios que NUM_RECOMANACIONS)
        limit = min(NUM_RECOMANACIONS, len(de_gran_a_petit))

        for x in range(limit):

            IDuser, similitud = de_gran_a_petit[x]

            dict_similituds[IDuser] = [similitud]

        # calcular mitjanes dels usuaris similars
        for IDuser, fila in usuaris_index.items():

            if IDuser in dict_similituds:

                fila_real = dades[fila, :]

                notes = fila_real[fila_real > 0]

                if len(notes) > 0:
                    mitjana_usuari = notes.mean()
                else:
                    mitjana_usuari = 0.0
                dict_similituds[IDuser].append(mitjana_usuari)

        # mitjana del usuari actual
        llista_user = dades[
            usuaris_index[self._usuari_a_comparar],
            :
        ]

        notes_user = llista_user[llista_user > 0]

        if len(notes_user) > 0:
            mitjana_user = notes_user.mean()
        else:
            mitjana_user = 0.0

        total_similituts = sum([s[0] for s in dict_similituds.values()])

        if total_similituts == 0:
            return

        fila_nou_usuari = dades[usuaris_index[self._usuari_a_comparar],:]

        for llibre, columna in books_index.items():

            # si ja l'ha valorat
            if fila_nou_usuari[columna] > 0:
                continue

            sumatori = 0

            for user, fila in usuaris_index.items():

                if user in dict_similituds:

                    nota = dades[fila, columna]

                    if nota > 0:

                        similitut = dict_similituds[user][0]

                        mitjana = dict_similituds[user][1]

                        sumatori += (similitut*(nota - mitjana))

            divisio = sumatori / total_similituts

            total = mitjana_user + divisio

            self._recomanacio_final[llibre] = total
           

#EL POSEM TMB A MOVIES?
    def __str__(self):

        resultat = ""
        ordenat = sorted(self._recomanacio_final.items(),key=lambda x: x[1],reverse=True)
        for llibre, score in ordenat:
            resultat += f"{llibre}: {score:.2f}\n"
        return resultat

class RecomanacioBasadaContingut_Book:
    def __init__(self):
        raise NotImplementedError("No és possible fer recomanació basada en contingut amb books per falta de dades")