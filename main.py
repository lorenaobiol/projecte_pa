#verificar que esta el data set
#pickle

import pickle
import os
from contingut import *
from config import *
from avaluacio import *
from gestionador import *
from recomanacio import *
import sys
import logging


def inicialitzar (nom_fitxer_pickle:str, tipus):

    if tipus is None:
        logging.warning("No s'ha introduït cap nombre al executar-lo")
        print('Ha hagut un error')
        return None
    
    if nom_fitxer_pickle and os.path.exists(nom_fitxer_pickle):
        with open(nom_fitxer_pickle, 'rb') as f: 
            gestionador = pickle.load(f) 
            logging.info(f"Gestionador carregat des de pickle: {nom_fitxer_pickle}")
        
        return gestionador
    
    if tipus==1:
        gestionador = Gestionador(tipus_contingut='MOVIES')
        gestionador.importar_dades('ratings.csv', ',')
        gestionador.importar_dades_contingut('movies.csv', ',')
        logging.info("Gestionador inicialitzat amb MovieLens100k")

    elif tipus==2:
        gestionador = Gestionador(tipus_contingut='BOOKS')
        gestionador.importar_dades('Ratings.csv', ',')
        gestionador.importar_dades_contingut('Books.csv', ',')
        logging.info("Gestionador inicialitzat amb Books")  
    
    with open(nom_fitxer_pickle, 'wb') as f:
        pickle.dump(gestionador, f)

        logging.info(f"Gestionador guardat a pickle: {nom_fitxer_pickle}")

    return gestionador

def main():

    entrada=input(f"Selecciona que vols fer:\n 1. Recomanacio, 2. Avaluacio. Per sortir introdueix qualsevol altra cosa.")
    logging.info(f"Entrada seleccionada: {entrada}")
    recomanador = None

    while entrada == '1' or entrada == '2':

        usuari=int(input('Ara, introdueix el id del usuari amb qui vols comparar:'))
        logging.info(f"Usuari seleccionat: {usuari}")

        if entrada == '1':   

            if metode == 1:
                recomanador = RecomanacioSimple(gestionador,usuari)
                logging.info(f"Recomanacio simple seleccionada per l'usuari: {usuari}") 
                
            elif metode == 2:
                recomanador = RecomanacioColaborativa(gestionador, usuari) 
                logging.info(f"Recomanacio col·laborativa seleccionada per l'usuari: {usuari}")

            elif metode == 3:
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

            metoder=input('De quina manera vols avaluar el teu recomanador? 1. MAE, 2. RMSE.')
            if not recomanador:
                logging.warning(f"Intent d'avaluació sense haver fet cap recomanació prèvia per l'usuari {usuari}")
                print('Primer has de fer una recomanacio per poder avaluar-la.')

            else:
                avaluacio = Avaluacio(recomanador, usuari, gestionador)
                logging.info(f"Avaluació inicialitzada per a l'usuari: {usuari} amb el recomanador: {type(recomanador).__name__}")

                if metoder == '1':
                    mae = avaluacio.calcular_MAE()
                    logging.info(f"Resultat de MAE: {mae}, calculat per a l'usuari {usuari}")
                    print(avaluacio)
                elif metoder == '2':
                    rmse = avaluacio.calcular_RMSE()
                    logging.info(f"Resultat de RMSE: {rmse}, calculat per a l'usuari {usuari}")
                    print(avaluacio)
                else:
                    logging.warning(f"Caràcter introduït no vàlid per a l'avaluació: {metode}")
                    print('Caràcter introduït no vàlid. Torna a intentar-ho.')
                    continue
        
        entrada=input(f"Selecciona que vols fer:\n 1. Recomanacio, 2. Avaluacio. Per sortir introdueix qualsevol altra cosa.")    

    else:
        logging.info("Programa finalitzat correctament")
        print('Fins aviat!')
            
if __name__ == "__main__":

    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('log '+ get_data() +'.txt'), 
        logging.StreamHandler()
    ]
)

    tipus=int(sys.argv[1]) if len(sys.argv) > 1 else None
    metode = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if tipus is None or tipus not in [1, 2]:
        print("Ha hagut un error amb el tipus, aquí s'explica l'ús correcte:")
        print("Per executar el programa, utilitza: python main.py tipus metode")
        print("Per seleccionar quina base dades vols analitzar has de escriure un d'aquests dos nombres:")
        print("Tipus de dades (1: MovieLens100k, 2: Books)")
        print("Torna a executar el programa seguint aquestes instruccions.")
        print('Si no carrega bé les dades, mira al gestionador i treu, o canvia, el path.\n')
        logging.warning(f"Tipus no vàlid: {tipus} ")

    elif metode is None or metode not in [1, 2, 3]:
        print("Ha hagut un error amb el mètode, aquí s'explica l'ús correcte:")
        print("Per executar el programa, utilitza: python main.py tipus metode")
        print(" Escull el mètode entre: ")
        print("1: Recomanació simple, 2: Recomanació col·laborativa, 3: Recomanació basada en contingut")
        print("Torna a executar el programa seguint aquestes instruccions.")
        logging.warning(f"Mètode no vàlid: {metode}")

    else:
        gestionador= inicialitzar('gestionador.pkl', tipus)
        main()

    logging.shutdown()


'''
- el rmse inclou les q son zero?
- podem avaluar davan de la recomnanacio en un usuari al que no hem fet la recomacio?
- fa falta logging a contingut?
- les cosees evidents cal documentar-les?


el logging tambe ha de sortir a la terminal
'''




