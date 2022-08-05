import datetime

def getDate() -> str:
    now = datetime.datetime.now()
    return now.strftime("%Y-%m")