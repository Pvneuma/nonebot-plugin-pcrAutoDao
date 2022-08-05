from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

from utils import db_util

autoDao = on_command("autoDao", aliases={"自动刀", "凹凸刀"}, priority=5, block=True)
addAuto = on_command("addAuto", aliases={"添加套餐"}, priority=4, block=True)


@autoDao.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    autoDao.send("")


@addAuto.got("set", prompt="是哪三个王呢？")
async def getSet(set: str = ArgPlainText("set")):
    boss_list = set.split(",")
    if len(boss_list) < 3:
        await addAuto.finish("套餐有问题哦，检查一下重新发送吧")


@addAuto.got("first", prompt="第一刀的阵容是？")
async def getFirstDao():
    pass


@addAuto.got("second", prompt="第二刀的阵容是？")
async def getSecondDao():
    pass


@addAuto.got("third", prompt="第三刀的阵容是？")
async def getThirdDao(set: str = ArgPlainText("set"), first: str = ArgPlainText("first"), second: str = ArgPlainText("second"), third: str = ArgPlainText("third")):
    await insert_set(set, first, second, third)
    await addAuto.finish("三刀记录好了哦")


async def insert_set(set: str, first: str, second: str, third: str):
    boss_list = set.split(",")
    dao = f'\n{boss_list[0]}：{first}\n{boss_list[1]}：{second}\n{boss_list[2]}：{third}'
    doc = {"set": set, "dao": dao}
    db_util.insert(doc)
