from ast import Dict
import asyncio
import os
import shutil
import subprocess

from services.log import logger

from .._path_config import PATH_, _IMAGE_PATH

async def download_azurapi_image() -> str:
    """# 实验功能

    下载[AzurAPI](https://github.com/AzurAPI/azurapi-js-setup/tree/master/images)的图片

    下载所有图片可能超过3个G，请确保网络稳定并且有足够的内存空间

    返回值:
        str: 返回错误信息，没有错误信息返回空值
    """
    try:
        shutil.rmtree(_IMAGE_PATH / "skills" / ".svn")
        shutil.rmtree(_IMAGE_PATH / "skins" / ".svn")
    except:
        pass
    retvalue = await asyncio.get_event_loop().run_in_executor(None, popen)
    return retvalue


def popen(timeout: str = 3600) -> str:
    url = "https://github.com/AzurAPI/azurapi-js-setup/trunk/images/"
    command = f"svn co {url}skills {url}skins image"
    # CREATE_NO_WINDOW = 0x08000000 if platform.system() == "Windows" else None
    cwd = str(PATH_.absolute())
    global p
    p = subprocess.Popen(
        command,
        # shell会导致无法kill
        # shell=True,
        cwd=cwd,
        # creationflags=CREATE_NO_WINDOW,
        )
    try:
        p.communicate(timeout=timeout)[0]
        if p.returncode == 0:
            logger.warning("碧蓝助手@图片更新完成！")
        else:
            logger.warning("碧蓝助手@图片更新失败，未知原因。请使尝试手动更新")
            return "碧蓝助手@片更新失败，未知原因。请使尝试手动更新"
    except:
        p.kill()
        logger.warning(f"碧蓝助手@图片资源下载超时，请尝试手动更新")
        return "碧蓝助手@图片资源下载超时"


def kill_popen():
    p.kill()
    

# from typing import Any
# from nonebot.exception import FinishedException
# from nonebot.adapters.onebot.v11 import Bot    
# @Bot.on_calling_api
# async def _(bot: Bot, api: str, data: Dict[str, Any]):
#     if not p and data["message"] in "碧蓝助手@片更新失败，未知原因。请使尝试手动更新":
#        raise FinishedException
