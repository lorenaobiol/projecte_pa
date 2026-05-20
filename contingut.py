from abc import ABC, abstractmethod
from typing import List, Dict

class Contingut(ABC):

    _titol: str

    def __init__(self, titol: str):
        self._titol = titol

    def get_titol(self): 
        return self._titol

    @abstractmethod
    def __str__(self) -> str:
        return NotImplementedError
     

class Llibre(Contingut):

    _isbn: str
    _autor: str 
    _any_publicacio: int
    

    def __init__(self, isbn: str, titol: str, autor: str, any_publicacio: int):
        super().__init__(titol)
        self._isbn = isbn
        self._autor = autor
        self._any_publicacio = any_publicacio
       
    def get_isbn(self): return self._isbn
    def get_autor(self): return self._autor
    def get_any(self): return self._any_publicacio
    
    def __str__(self) -> str: return f"{self._titol} ({self._autor}, {self._any_publicacio})"
    

class Movie(Contingut):

    _movie_id: int
    _generes: List[str]

    def __init__(self, movie_id: int, titol: str, generes: List[str]):
        super().__init__(titol)
        self._movie_id = movie_id
        self._generes = generes

    def get_movie_id(self): return self._movie_id
    def get_generes(self): return self._generes
    
    def __str__(self) -> str: return f"{self._titol} ({', '.join(self._generes)})"


