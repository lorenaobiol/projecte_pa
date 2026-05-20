from typing import List, Dict

class Usuari:

    _user_id: int
    _puntuacions: dict

    def __init__(self, user_id: int, puntuacions: dict):
        self._user_id = user_id
        self._puntuacions= puntuacions


    def get_user_id(self): 
        return self._user_id
    def get_punutaciosn(self): 
        return self._puntuacions
    def get_edat(self): 
        return self._edat