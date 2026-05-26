#parametres globals

MIN_VOTS=3 #simple
NUM_RECOMANACIONS=5 #simple i colab
sep=','
LIMIT=10000
PMAX=5

from datetime import datetime
def get_data():
    date_time = datetime.now()
    str_date_time = date_time.strftime("%d-%m-%Y, %H.%M.%S")
    return str_date_time