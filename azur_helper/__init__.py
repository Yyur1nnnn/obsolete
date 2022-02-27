from nonebot.plugin import CommandGroup
from nonebot.plugin.on import on_command
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Message, MessageEvent

from .names import *


Azur = CommandGroup("azur", priority=5, block=True)
azur_ = Azur.command("",aliases={"/碧蓝"}, priority=6)



@azur_.handle()
async def _(args: Message = CommandArg()):
    args = str(args).split()
    nickname_list=skin_list = ""
    ship_name = str(args[0])
    print(ship_name)
    ship_nickname_data = await GetIDByNickname(ship_name)
    if ship_nickname_data:
        if len(args) == 1:
            ship_nickname_list = await GetAllNickname(ship_nickname_data["id"])
            for string in ship_nickname_list:
                nickname_list+=(str(string)+"\n")
            ship_skin_list = await GetIDBySkins(ship_nickname_list[0])
            for string in ship_skin_list:
                skin_list+=(str(string)+"\n")
            # 打印
        elif len(args) == 2:
            pass
        else:
            await azur_.finish(
                "查询出错！查询命令仅支持两个参数。例：azur [舰名] ?[皮肤]",
                at_sender=True
            )
    else:
        await azur_.finish(
            "查询出错，好像没有这艘船呢，如果想为她新增昵称请发送： blhx备注 正式船名 昵称",
            at_sender=True
        )
