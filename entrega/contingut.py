from abc import ABC, abstractmethod
from typing import List, Dict

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


