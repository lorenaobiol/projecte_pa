from abc import ABC, abstractmethod
from typing import List, Dict
import csv


#fem amb numpy i llibres fem dins 10 mil i busquem usuari
class Gestionador:

    _matriu_dades: list
    _dict_contingut: Dict[str, 'Contingut']
    _dict_usuaris: Dict[int, 'Usuari']
    _usuari_index: Dict[int, int]
    _contingut_index: Dict[str, int]

    def __init__(self):
        self._matriu_dades = []
        self._dict_contingut = {}
        self._dict_usuaris = {}
        self._usuari_index  = {}
        self._contingut_index = {}


    
    def importar_dades(self, nomfitxer,sep):
    
        usuari_index = dict()
        idcont_index = dict()
        matriu_dades = dict()

        with open(nomfitxer, "r", encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=sep)
            next(csv_reader)  

            for linia in csv_reader:
                user_id = int(linia[0])
                idcont = linia[1]
                rating = float(linia[2])

                if user_id not in usuari_index:
                    usuari_index[user_id] = len(usuari_index)

                if idcont not in idcont_index:
                    idcont_index[idcont] = len(idcont_index)

                fila = usuari_index[user_id]
                columna = idcont_index[idcont]

                if fila not in matriu_dades:
                    matriu_dades[fila] = dict()

                matriu_dades[fila][columna] = rating
        
        self._matriu_dades = matriu_dades
        self._usuari_index = usuari_index
        self._contingut_index = idcont_index

    def get_matriu_dades(self): 
        return self._matriu_dades
    def get_dict_contingut(self): 
        return self._dict_contingut
    def get_dict_usuaris(self): 
        return self._dict_usuaris
    def get_usuari_index(self): 
        return self._usuari_index
    def get_contingut_index(self): 
        return self._contingut_index

    #def importar_dades_contingut(self, nomfitxer,sep):
    #def importar_dades_usuaris(self, nomfitxer,sep):
    #getters




class Contingut(ABC):

    _nom: str

    def __init__(self, nom: str):
        self._nom = nom

    def get_nom(self): 
        return self._nom

    @abstractmethod
    def __str__(self) -> str:
        return NotImplementedError
     

class Llibre(Contingut):

    _isbn: str
    _autor: str 
    _any_publicacio: int
    _publicador: str
    _imatges: List[str]

    def __init__(self, isbn: str, titol: str, autor: str, any_publicacio: int, publicador: str, imatges: List[str]):
        super().__init__(titol)
        self._isbn = isbn
        self._autor = autor
        self._any_publicacio = any_publicacio
        self._publicador = publicador
        self._imatges = imatges #mirar be com ficar les imatges. desde el gestionador

    def get_isbn(self): 
        return self._isbn
    def get_autor(self): 
        return self._autor
    def get_any(self): 
        return self._any_publicacio
    def get_publicador(self): 
        return self._publicador
    def get_imatges(self): 
        return self._imatges

class Pelicula(Contingut):

    _movie_id: int
    _generes: List[str]

    def __init__(self, movie_id: int, titol: str, generes: List[str]):
        super().__init__(titol)
        self._movie_id = movie_id
        self._generes = generes

    def get_movie_id(self): 
        return self._movie_id
    def get_generes(self): 
        return self._generes


class Usuari:

    _user_id: int
    _localitzacio: str
    _edat: float

    def __init__(self, user_id: int, localitzacio: str, edat: float):
        self._user_id = user_id
        self._localitzacio = localitzacio
        self._edat = edat

    def get_user_id(self): 
        return self._user_id
    def get_localitzacio(self): 
        return self._localitzacio
    def get_edat(self): 
        return self._edat


class Recomanacio(ABC):

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




class RecomanacioSimple(Recomanacio):
    _avg_general: float
    _avg_item: dict
    _num_vots: int
    _min_vots:int

    def __init__(self,gestionador: Gestionador):
        super().__init__(gestionador)
        self._dict_contingut: dict = {}
        self._avg_general=0
        self._avg_item={}
        self._num_vots=0
        self._min_vots=0

    def trobar_similituds(self,min_vots:int, usuari:Usuari): #importa si al int que entro li canvio el nom?
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
        self._min_vots=k
        
    def calcular_recomanacio(self):
        primera_part=((self._num_vots/(self._num_vots+self._min_vots))*self._avg_item)
        segona_part=((self._min_vots/(self._num_vots+self._min_vots))*self._avg_general)

        self._recomanacio_final=primera_part+segona_part

    def __str__(self):
        #????
        return '\n'.join([str(x) for x in self._recomanacio_final])


class RecomanacioColaborativa(Recomanacio):

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



                
        

        
    


#class RecomanacioColaborativa(Recomanacio):