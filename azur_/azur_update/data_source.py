import json
import os
from pathlib import Path
import aiofiles

from services.log import logger
from utils.http_utils import AsyncHttpx
from utils.utils import get_bot, scheduler

from .._path_config import _DATA_PATH
from .update_image import download_azurapi_image, popen
from .update_data import update_name_dict


async def get_local_version() -> int:
    """
    获取本地版本信息

    返回值:
        int: 版本号
    """
    async with aiofiles.open(_DATA_PATH / "version-info.json",
                             'r',
                             encoding='utf-8') as lf:
        load_dict = json.loads(await lf.read())
    return load_dict['ships']['version-number']


async def compare_version() -> bool:
    """
    获取GitHub版本信息与本地版本进行比较

    返回值:
        bool: 比较结果
    """
    try:
        varurl = "https://cdn.jsdelivr.net/gh/AzurAPI/azurapi-js-setup@master/version-info.json"
        data = (await AsyncHttpx.get(varurl)).json()
        gitver = data['ships']['version-number']
        localver = await get_local_version()
        if gitver <= localver:
            return False
    except:
        pass
    return True


async def send_superusers(message: str = None):
    await get_bot().send_private_msg(user_id=int(
        list(get_bot().config.superusers)[0]),
                                     message=message)


async def update_local_resources(skipif: bool = False):
    """
    更新本地数据和图片资源

    参数:
        skipif (bool, optional): 是否跳过版本比较直接更新，因为强制模式已经比较过一次版本
        所以可以选择直接更新。
    """
    if skipif or compare_version():
        url = "https://github.com/AzurAPI/azurapi-js-setup"
        #优先更新数据
        await send_superusers("碧蓝助手@正在更新碧蓝助手资源，请保证网络可以链接到github并且内存充足 \n" +
                              f"期间如果出现报错，请前往{url}手动更新资源")
        err = await update_name_dict()
        if err:
            await send_superusers(err)
        else:
            logger.info(f"数据文件更新完成，开始下载图片资源")
        await send_superusers(f"准备开始下载图片文件，下载期间可以在任意聊天中发送【取消碧蓝图片更新】中断")
        #下载图片
        set_update_state(True, "download_image")
        err = await download_azurapi_image()
        if err:
            await send_superusers(err + f"\n请前往{url}往手动更新")
        else:
            version = await get_local_version()
            await send_superusers(f"碧蓝助手@当前更新已完成，当前版本为{version}。")
        set_update_state(False, "download_image")


path_ = Path(__file__).parent
UPDATE_STATE = path_ / "update_state.json"


def get_update_state(task: str = "apscheduler") -> bool:
    """
    返回当前某个更新任务是否进行，默认返回定时更新的开启状态

    参数:
        task (str, optional): 要获取的任务名，默认为定时任务

    返回值:
        bool: 任务是否正在进行
    """
    try:
        return json.load(open(UPDATE_STATE))[task]
    except:
        return False


def set_update_state(state: bool, task: str = "apscheduler"):
    """
    设定某个任务的进行状态，默认为定时任务

    参数:
        state (bool): 设定的状态
        task (str, optional): 要设定的任务名，默认为定时任务
    """
    data = json.load(open(UPDATE_STATE)) if os.path.isfile(UPDATE_STATE) \
        else {"apscheduler": False, "download_image": False}
    data[task] = state
    json.dump(data, open(UPDATE_STATE, "w"))


# 判断定时任务是否开启
def apscheduler_switch():
    if get_update_state():
        scheduler.add_job(
            update_local_resources,
            "cron",
            # day_of_week=3,
            hour=2,
            id="azur_update")
    else:
        try:
            scheduler.remove_job("azur_update")
        except:
            pass


apscheduler_switch()
