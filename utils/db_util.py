import pymongo
from .date_util import getDate

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["nonebot-plugin-pcrAutoDao"]


def get_col():
    date = getDate()
    return mydb[date]


async def insert(doc):
    col = get_col()
    col.insert_one(doc)


async def get_all():
    col = get_col()
    return col.find()


async def get_by_set(set: str):
    col = get_col()
    row = col.find({"set": set})
    rows = []
    for x in row:
        rows.append(x)
    return rows


async def delete_row(set: str, dao: str):
    col = get_col()
    res = col.delete_one({"set": set, "dao": dao}).deleted_count
    return res==1
