import re
from colorama import Cursor
import pymongo
from .date_util import getDate

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["nonebot-plugin-pcrAutoDao"]


def get_col():
    date = getDate()
    return mydb["test"]


def insert(doc):
    col = get_col()
    col.insert_one(doc)


async def get_all():
    col = get_col()
    return col


def get_by_set(set: str):
    col = get_col()
    row = col.find({"set": set})
    return row[0]

print("123")