from nonebot import on_command, on_shell_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message, Event
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER

from .utils import db_util

autoDao = on_command("autoDao", aliases={
                     "查自动刀", "查凹凸刀"}, priority=5, block=True)
addSet = on_command("addSet", aliases={"添加套餐"}, priority=4, block=True)
dropAuto = on_command("dropSet", aliases={
                      "删除套餐"}, priority=6, block=True)

lastQuery = {}


@autoDao.handle()
async def handle_autoDao(state: T_State):
    set_list = await get_sets()
    if len(set_list) == 0:
        await autoDao.finish("当前还没有套餐哦")
    state["set_list"] = set_list
    msg = ""
    i = 1
    for x in set_list:
        msg += f'{i}. {x}'
        if i != len(set_list):
            msg += '\n'
        i += 1
    await autoDao.send(msg)


@autoDao.got("index")
async def handle_query(state: T_State, event: Event, index: str = ArgPlainText("index")):
    try:
        i = int(index)-1
        set = state["set_list"][i]
    except:
        autoDao.finish("套餐号好像不对呢")
    rows = await db_util.get_by_set(set)
    msg = ""
    i = 1
    for row in rows:
        msg += row["dao"]
        if i != len(rows):
            msg += "\n\n"
        i += 1
    lastQuery[event.get_user_id] = rows
    await autoDao.finish(msg)


@addSet.got("set", prompt="是哪三个王呢？")
async def getSet(set: str = ArgPlainText("set")):
    boss_list = set.split(",")
    if len(boss_list) < 3:
        await addSet.finish("套餐有问题哦，检查一下重新发送吧")


@addSet.got("first")
async def getFirstDao():
    pass


@addSet.got("second")
async def getSecondDao():
    pass


@addSet.got("third")
async def getThirdDao(set: str = ArgPlainText("set"), first: str = ArgPlainText("first"), second: str = ArgPlainText("second"), third: str = ArgPlainText("third")):
    await insert_set(set.upper(), first, second, third)
    await addSet.finish("三刀记录好了哦")


async def insert_set(set: str, first: str, second: str, third: str):
    boss_list = set.split(",")
    dao = f'{boss_list[0]}：{first}\n{boss_list[1]}：{second}\n{boss_list[2]}：{third}'
    doc = {"set": set, "dao": dao}
    await db_util.insert(doc)


async def get_sets():
    col = await db_util.get_all()
    temp = set()
    for x in col:
        temp.add(f'{x["set"]}')
    return list(temp)


@dropAuto.handle()
async def handle_drop_set(event: Event, arg: Message = CommandArg()):
    arg = arg.extract_plain_text().strip()
    try:
        rows = lastQuery[event.get_user_id]
    except:
        dropAuto.finish("好像还没查询过自动刀呢")
    try:
        if arg != '':
            i = int(arg)
            row = rows[i-1]
        else:
            row = rows[0]
    except:
        dropAuto.finish("序号好像不对呢")
    res = await db_util.delete_row(row["set"], row["dao"])
    if res:
        msg="删除成功"
    else:
        msg="删除失败"
    await dropAuto.finish(msg)
