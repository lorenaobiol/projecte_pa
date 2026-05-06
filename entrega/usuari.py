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