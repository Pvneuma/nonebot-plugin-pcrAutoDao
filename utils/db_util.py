from colorama import Cursor
import pymongo
from .date_util import getDate

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["nonebot-plugin-pcrAutoDao"]


def get_col():
    date = getDate()
    return mydb["test"]


async def insert(doc):
    col = get_col()
    col.insert_one(doc)


async def get_all():
    col = get_col()
    return col


async def get_by_set(set:str)->dict:
    col = get_col({"set":set})
    for x in col:
        res=x
        break
    return res
