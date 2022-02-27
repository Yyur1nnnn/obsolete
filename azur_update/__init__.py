from re import T
from utils.utils import scheduler
from nonebot.matcher import Matcher
from nonebot.exception import FinishedException
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Message
from nonebot.plugin.on import on_command, on_regex
from nonebot.params import Arg, ArgPlainText, CommandArg

from .data_source import get_update_state, set_update_state, update_local_resources, apscheduler_switch
from .update_image import kill_popen


update = on_command("更新碧蓝数据", priority=5, block=True, permission=SUPERUSER)
cancel_download_image = on_command("取消碧蓝图片更新", priority=5, block=True, permission=SUPERUSER)

@update.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    plain_text = arg.extract_plain_text()
    if plain_text:
        matcher.set_arg("mod", arg)
       
     
@update.got("mod", prompt="请选择模式[强制|定时]")
async def _(mod: str = ArgPlainText("mod")):
    if not mod in r"(强制|定时)$":
        await update.send("参数错误,默认以强制模式更新", at_sender=True)
        mod = "强制"
    if "强制" == mod:
        await update.send("已选择强制模式更新", at_sender=True)
        await update_local_resources()
        raise FinishedException
    else: 
        state = get_update_state()
        state_text = "开启" if state else "关闭"
        nstate_text = "关闭" if state else "开启"
        message = f"当前定时更新已{state_text}，是否{nstate_text}？[是*/否n]"
        await update.send(message=message)
        update.skip()


#定时下载开关
@update.got("update_state")
async def _(update_state: str = ArgPlainText("update_state")):
    # 当前定时更新已{state}，是否{not_state}？[是*/否n]
    bool_ = False if update_state in r"(否|[n|N][o|O]|[n|N])" else True
    state = False if set_update_state() else True
    if bool_:
        message = "操作已取消"
    else: 
        set_update_state(state)
        apscheduler_switch()
        state_text = "开启" if state else "关闭"
        message = f"碧蓝助手@当前定时更新已{state_text}"
    await update.finish(message, at_sender=True)
    

#取消svn co的进程
@cancel_download_image.handle()
async def _():
    if get_update_state("download_image"):
        kill_popen()
        await cancel_download_image.finish(
            "以取消当前图片更新",
            at_sender=True
        )
    else:
        await cancel_download_image.finish(
            "现在还没有图片更新任务呢！",
            at_sender=True
        )
