from abc import ABC, abstractmethod
from typing import List, Dict
import logging
from config import *

logging.basicConfig(

    filename='log '+ get_data() +'.txt',
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    #handlers= [logging.FileHandler('log '+ get_data() +'.txt'), 
              #logging.StreamHandler()] 
    ) #ferho en una linia

class Contingut(ABC):
    """
    Classe abstracta que representa un contingut genèric amb títol.
    """

    _titol: str

    def __init__(self, titol: str):
        """
        Inicialitza el contingut amb un títol.
        """
        logging.debug(f"Inicialitzant Contingut amb títol: {titol}")
        self._titol = titol

    def get_titol(self): 
        """
        Retorna el títol del contingut.
        """
        logging.debug(f"Retornant títol: {self._titol}")
        return self._titol

    @abstractmethod
    def __str__(self) -> str:
        """
        Mètode abstracte que retorna una representació en text del contingut.
        """
        return NotImplementedError
     

class Llibre(Contingut):
    """
    Classe que representa un llibre amb isbn, autor i any de publicació.
    """

    _isbn: str
    _autor: str 
    _any_publicacio: int
    

    def __init__(self, isbn: str, titol: str, autor: str, any_publicacio: int):
        """
        Inicialitza el llibre amb isbn, títol, autor i any de publicació.
        """
        super().__init__(titol)
        self._isbn = isbn
        self._autor = autor
        self._any_publicacio = any_publicacio

       
    def get_isbn(self): return self._isbn
    def get_autor(self): return self._autor
    def get_any(self): return self._any_publicacio
    
    def __str__(self) -> str: return f"{self._titol} ({self._autor}, {self._any_publicacio})"
    

class Movie(Contingut):
    """
    Classe que representa una pel·lícula amb identificador i gèneres.
    """

    _movie_id: int
    _generes: List[str]

    def __init__(self, movie_id: int, titol: str, generes: List[str]):
        """
        Inicialitza la pel·lícula amb un identificador, títol i llista de gèneres.
        """
        super().__init__(titol)
        self._movie_id = movie_id
        self._generes = generes

    def get_movie_id(self): return self._movie_id
    def get_generes(self): return self._generes
    
    def __str__(self) -> str: return f"{self._titol} ({', '.join(self._generes)})"


