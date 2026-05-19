#verificar que esta el data set
#pickle

import pickle
import os
from abc import ABC, abstractmethod
from typing import List, Dict
import csv
from entrega.contingut import *
from entrega.config import *
from entrega.avaluacio import *
from entrega.gestionador import *
from entrega.recomanacio import *
import numpy as np

def inicialitzar (nom_fitxer_pickle:str):
    if nom_fitxer_pickle and os.path.exists(nom_fitxer_pickle):
        with open(nom_fitxer_pickle, 'rb') as f: 
            gestionador = pickle.load(f) #logging -> sha fet correctament
        return gestionador
    
    print('Selecciona quina base dades vols analitzar:')
    tipus = input("Tipus de dades (1: MovieLens100k, 2: Books): ")
    print('Has seleccionat la base de dades MovieLens100k, ara, selecciona el mètode de recomanació:')  
    metode = input("Mètode de recomanació (1: Simple, 2: Col·laboratiu, 3: Basat en contingut): ")
        
    
    if tipus==1:
        gestionador = Gestionador(int_idcont='MOVIES')
        gestionador.importar_dades('ratings.csv', ',')
        gestionador.importar_dades_contingut('movies.csv', ',')
    elif tipus==2:
        gestionador = Gestionador(int_idcont='BOOKS')
        gestionador.importar_dades('Ratings.csv', ',')
        
    
    with open(nom_fitxer_pickle, 'wb') as f:
        pickle.dump(gestionador, f) #logging -> sha fet correctament

    return gestionador, metode

gestionador, metode = inicialitzar('gestionador.pkl')

if metode == 1:
    recomanador = RecomanacioSimple(gestionador) 
    RecomanacioSimple.trobar_similituds()
    final=RecomanacioSimple.calcular_recomanacio()
    print(final)   
elif metode == 2:
    recomanador = RecomanacioColaborativa(gestionador)
    usuari=input('Introdueix el id del usuari amb qui vols comparar:')
elif metode == 3:
    recomanador = RecomanacioBasadaContingut(gestionador)
    usuari=input('Introdueix el id del usuari amb qui vols comparar:')



