"""
Mòdul d'avaluació.

Aquest fitxer permet calcular mètriques
d'avaluació sobre les recomanacions:
- MAE
- RMSE
"""

from entrega.contingut import *
from entrega.config import *
from entrega.recomanacio import *
from entrega.gestionador import *

import numpy as np

from abc import ABC, abstractmethod
from typing import List, Dict
from math import abs, sqrt


class Avaluacio(ABC):
    """
    Classe encarregada d'avaluar recomanacions.

    Attributes:
        _resultat_MAE (float):
            Resultat del càlcul MAE.

        _resultat_RMSE (float):
            Resultat del càlcul RMSE.

        _recomanador (Recomanacio):
            Recomanador utilitzat.

        _punt_usuari (List):
            Llista de puntuacions de l'usuari.
    """

    _resultat_MAE: float
    _resultat_RMSE: float
    _recomanador: Recomanacio
    _punt_usuari: List

    def __init__(
        self,
        recomanador: Recomanacio,
        iduser: int,
        gestionador: Gestionador
    ):
        """
        Inicialitza l'avaluació.

        Args:
            recomanador (Recomanacio):
                Recomanador a avaluar.

            iduser (int):
                ID de l'usuari.

            gestionador (Gestionador):
                Gestionador de dades.
        """

        # Inicialitzar resultat del MAE
        self._resultat_MAE = 0

        # Inicialitzar resultat del RMSE
        self._resultat_RMSE = 0

        # Guardar recomanador utilitzat
        self._recomanador = recomanador

        # Guardar puntuacions de l'usuari
        self._punt_usuari = (
            gestionador.get_matriu_dades()[
                gestionador.get_usuari_index()[iduser],
                :
            ]
        )

    def calcular_MAE(self):
        """
        Calcula el MAE (Mean Absolute Error).

        Returns:
            float:
                Valor del MAE.
        """

        # Obtenir recomanacions finals
        dict_recomanacio = (
            self._recomanador.get_recomanacio_final()
        )

        # Calcular suma dels errors absoluts
        sumatori = sum(

            abs(p_reco - p_usuari)

            for p_reco, p_usuari in zip(
                dict_recomanacio.values(),
                self._punt_usuari
            )

            # Només comptem puntuacions existents
            if p_usuari != 0
        )

        # Llista d'items valorats per l'usuari
        items = [
            it
            for it in self._punt_usuari
            if it != 0
        ]

        # Fórmula del MAE
        self._resultat_MAE = (
            sumatori / len(items)
        )

        return self._resultat_MAE

    def calcular_RMSE(self):
        """
        Calcula el RMSE
        (Root Mean Squared Error).

        Returns:
            float:
                Valor del RMSE.
        """

        # Obtenir recomanacions finals
        dict_recomanacio = (
            self._recomanador.get_recomanacio_final()
        )

        # Calcular suma dels errors al quadrat
        sumatori = sum(

            (p_reco - p_usuari) ** 2

            for p_reco, p_usuari in zip(
                dict_recomanacio.values(),
                self._punt_usuari
            )

            # Només comptem puntuacions existents
            if p_usuari != 0
        )

        # Llista d'items valorats per l'usuari
        items = [
            it
            for it in self._punt_usuari
            if it != 0
        ]

        # Fórmula del RMSE
        self._resultat_RMSE = sqrt(
            sumatori / len(items)
        )

        return self._resultat_RMSE