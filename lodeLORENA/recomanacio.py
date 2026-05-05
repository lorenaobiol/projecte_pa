from abc import ABC, abstractmethod
from typing import List, Dict

class Gestionador:
    def __init__(self):
        self._matriu_dades: list = []
        self._llista_contingut: Dict[str, Contingut] = {}
        self._llista_usuaris: Dict[int, Usuari] = {}
        self._usuari_index: Dict[int, int] = {}
        self._contingut_index: Dict[str, int] = {}

class Contingut(ABC):
    def __init__(self, nom: str):
        self._nom = nom

    def get_nom(self): 
        return self._nom

    @abstractmethod
    def __str__(self) -> str:
        return NotImplementedError
     

class Llibre(Contingut):
    def __init__(self, isbn: str, titol: str, autor: str, any_publicacio: int, publicador: str, imatges: List[str]):
        super().__init__(titol)
        self._isbn = isbn
        self._autor = autor
        self._any_publicacio = any_publicacio
        self._publicador = publicador
        self._imatges = imatges
#TOTA LA INFO ENS CAL DESPRÉS?
    def get_isbn(self): 
        return self._isbn
    def get_autor(self): 
        return self._autor
    def get_any(self): 
        return self._any_publicacio
    def get_publicador(self): 
        return self._publicador
#CAL?? MIRAR BÉ EL Q ES 
    def get_imatges(self): 
        return self._imatges

class Pelicula(Contingut):
    def __init__(self, movie_id: int, titol: str, generes: List[str]):
        super().__init__(titol)
        self._movie_id = movie_id
        self._generes = generes

    def get_movie_id(self): 
        return self._movie_id
    def get_generes(self): 
        return self._generes


class Usuari:
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
    def __init__(self):
        self._recomanacio_final = []



class RecomanacioSimple(Recomanacio):
    def __init__(self):
        super().__init__()
        self._dict_contingut: dict = {}

class RecomanacioColaborativa(Recomanacio):
    def __init__(self):
        super().__init__()
        self._usuaris_similars: List = []
class RecomanacioColaborativa(Recomanacio):


