import pymongo
from date_util import getDate

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["nonebot-plugin-pcrAutoDao"]

def get_col():
    date=getDate()
    return mydb["test"]

def insert(doc):
    col=get_col()
    col.insert_one(doc)

def getAll():
    col=get_col()
    for x in col.find():
        print(x)
