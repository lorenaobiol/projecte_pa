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

logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)

def inicialitzar (nom_fitxer_pickle:str):
    if nom_fitxer_pickle and os.path.exists(nom_fitxer_pickle):
        with open(nom_fitxer_pickle, 'rb') as f: 
            gestionador = pickle.load(f) 
            logging.info(f"Gestionador carregat des de pickle: {nom_fitxer_pickle}")
        
        return gestionador
    
    print('Selecciona quina base dades vols analitzar:')
    tipus = int(input("Tipus de dades (1: MovieLens100k, 2: Books): "))
    
    
    if tipus==1:
        gestionador = Gestionador(int_idcont='MOVIES')
        gestionador.importar_dades('ratings.csv', ',')
        gestionador.importar_dades_contingut('movies.csv', ',')

        logging.info("Gestionador inicialitzat amb MovieLens100k")
    elif tipus==2:
        gestionador = Gestionador(int_idcont='BOOKS')
        gestionador.importar_dades('Ratings.csv', ',')

        logging.info("Gestionador inicialitzat amb Books")
    else:
        print('Tipus de dades no valid. Torna a intentar-ho.')

        logging.warning(f"Tipus de dades no valid: {tipus}")
        
        return inicialitzar(nom_fitxer_pickle)
        
    
    with open(nom_fitxer_pickle, 'wb') as f:
        pickle.dump(gestionador, f)

        logging.info(f"Gestionador guardat a pickle: {nom_fitxer_pickle}")

    return gestionador


gestionador= inicialitzar('gestionador.pkl')

print('A continuació, selecciona que vols fer:')
print(f"Per a poder seleccionar el metode d'avaluació primer has d'haver fer una recomanació")
entrada=input('1. Recomanacio, 2. Avaluacio. ')
logging.info(f"Entrada seleccionada: {entrada}")
recomanador = None


while entrada == '1' or entrada == '2':

    usuari=int(input('Ara, introdueix el id del usuari amb qui vols comparar:'))
    logging.info(f"Usuari seleccionat: {usuari}")

    if entrada == '1':     
        metode=input('Selecciona el metode de recomanacio que vols utilitzar: 1. Recomanacio simple, 2. Recomanacio col·laborativa, 3. Recomanacio basada en contingut. ')
        if metode == '1':
            recomanador = RecomanacioSimple(gestionador,usuari)
            logging.info(f"Recomanacio simple seleccionada per l'usuari: {usuari}") 
            
        elif metode == '2':
            recomanador = RecomanacioColaborativa(gestionador, usuari) 
            logging.info(f"Recomanacio col·laborativa seleccionada per l'usuari: {usuari}")

        elif metode == '3':
            recomanador = RecomanacioBasadaContingut(gestionador,usuari)
            logging.info(f"Recomanacio basada en contingut seleccionada per l'usuari: {usuari}")
        
        else:
            logging.warning(f"Caràcter introduït no vàlid: {metode}")
            print('Caràcter introduït no vàlid. Torna a intentar-ho.')
            continue

        recomanador.trobar_similituds()
        recomanador.calcular_recomanacio()
        logging.info(f"Recomanacio calculada per a l'usuari: {usuari}")
        print(recomanador)

    elif entrada == '2':

        metode=input('De quina manera vols avaluar el teu recomanador? 1. MAE, 2. RMSE.')
        if not recomanador:
            logging.warning(f"Intent d'avaluació sense haver fet cap recomanació prèvia per l'usuari {usuari}")
            print('Primer has de fer una recomanacio per poder avaluar-la.')

        else:
            avaluacio = Avaluacio(recomanador, usuari, gestionador)
            logging.info(f"Avaluació inicialitzada per a l'usuari: {usuari} amb el recomanador: {type(recomanador).__name__}")

            if metode == '1':
                mae = avaluacio.calcular_MAE()
                logging.info(f"Resultat de MAE: {mae}, calculat per a l'usuari {usuari}")
                print(avaluacio)
            elif metode == '2':
                rmse = avaluacio.calcular_RMSE()
                logging.info(f"Resultat de RMSE: {rmse}, calculat per a l'usuari {usuari}")
                print(avaluacio)
            else:
                logging.warning(f"Caràcter introduït no vàlid per a l'avaluació: {metode}")
                print('Caràcter introduït no vàlid. Torna a intentar-ho.')
                continue
    
    entrada=input('Iara que vols fer? 1. Recomanacio, 2. Avaluacio. // Per sortir introdueix qualsevol altra cosa. ')
            

else:
    logging.info("Programa finalitzat correctament")
    print('Fins aviat!')
        






