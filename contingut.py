from abc import ABC, abstractmethod
from typing import List, Dict
import logging
from config import *


class Contingut(ABC):
    """Classe abstracta que representa un contingut genèric amb títol.
 
    Attributes:
        _titol (str): Títol del contingut.
    """

    _titol: str

    def __init__(self, titol: str):
        """Inicialitza el contingut amb un títol.
 
        Args:
            titol (str): Títol del contingut.
        """
        logging.debug(f"Inicialitzant Contingut amb títol: {titol}")
        self._titol = titol

    def get_titol(self): 
        """Retorna el títol del contingut.
 
        Returns:
            str: Títol del contingut.
        """
        logging.debug(f"Retornant títol: {self._titol}")
        return self._titol

    @abstractmethod
    def __str__(self) -> str:
        """Retorna una representació en text del contingut.
 
        Raises:
            NotImplementedError: Si la subclasse no implementa aquest mètode.
        """
        raise NotImplementedError
     

class Llibre(Contingut):
    """Classe que representa un llibre amb ISBN, autor i any de publicació.
 
    Attributes:
        _isbn (str): Codi ISBN identificador del llibre.
        _autor (str): Nom de l'autor del llibre.
        _any_publicacio (int): Any de publicació del llibre.
    """

    _isbn: str
    _autor: str 
    _any_publicacio: int
    

    def __init__(self, isbn: str, titol: str, autor: str, any_publicacio: int):
        """Inicialitza el llibre amb ISBN, títol, autor i any de publicació.
 
        Args:
            isbn (str): Codi ISBN identificador del llibre.
            titol (str): Títol del llibre.
            autor (str): Nom de l'autor del llibre.
            any_publicacio (int): Any de publicació del llibre.
        """
        super().__init__(titol)
        self._isbn = isbn
        self._autor = autor
        self._any_publicacio = any_publicacio

       
    def get_isbn(self):
        """Retorna el codi ISBN del llibre.
 
        Returns:
            str: Codi ISBN del llibre.
        """ 
        
        return self._isbn
    
    def get_autor(self):
        """Retorna el nom de l'autor del llibre.
 
        Returns:
            str: Nom de l'autor del llibre.
        """ 
        
        return self._autor
    
    def get_any(self): 
        """Retorna l'any de publicació del llibre.
 
        Returns:
            int: Any de publicació del llibre.
        """
        
        return self._any_publicacio
    
    def __str__(self) -> str:
        """Retorna una representació en text del llibre.
 
        Returns:
            str: Cadena amb el títol, autor i any de publicació del llibre.
                 Format: "Títol (Autor, Any)".
        """ 
        
        return f"{self._titol} ({self._autor}, {self._any_publicacio})"
    

class Movie(Contingut):
    """Classe que representa una pel·lícula amb identificador i gèneres.
 
    Attributes:
        _movie_id (int): Identificador únic de la pel·lícula.
        _generes (List[str]): Llista de gèneres als quals pertany la pel·lícula.
    """

    _movie_id: int
    _generes: List[str]

    def __init__(self, movie_id: int, titol: str, generes: List[str]):
        """Inicialitza la pel·lícula amb un identificador, títol i llista de gèneres.
 
        Args:
            movie_id (int): Identificador únic de la pel·lícula.
            titol (str): Títol de la pel·lícula.
            generes (List[str]): Llista de gèneres als quals pertany la pel·lícula.
        """
        super().__init__(titol)
        self._movie_id = movie_id
        self._generes = generes

    def get_movie_id(self): 
        """Retorna l'identificador únic de la pel·lícula.
 
        Returns:
            int: Identificador únic de la pel·lícula.
        """
        return self._movie_id
    def get_generes(self): 
        """Retorna la llista de gèneres de la pel·lícula.
 
        Returns:
            List[str]: Llista de gèneres de la pel·lícula.
        """
        return self._generes
    
    def __str__(self) -> str:
        """Retorna una representació en text de la pel·lícula.
 
        Returns:
            str: Cadena amb el títol i els gèneres de la pel·lícula.
                 Format: "Títol (Gènere1, Gènere2, ...)".
        """
        return f"{self._titol} ({', '.join(self._generes)})"


