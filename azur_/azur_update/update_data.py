import json
from pathlib import Path
import aiofiles
from bs4 import BeautifulSoup

from services.log import logger
from utils.http_utils import AsyncHttpx

from .._path_config import _DATA_PATH


async def download_azurapi_data() -> bool:
    """
    
    下载AzurAPI的json数据
    
    """

    # https://raw.fastgit.org可以根据需要配置不同代理，结合网络情况自行修改
    main_url = "https://cdn.jsdelivr.net/gh/AzurAPI/azurapi-js-setup@master/"
    josn_list = [
        "chapters.json",
        "equipments.json",
        "version-info.json",
        "memories.json",
        "ships.json",
    ]

    logger.info(f"正在从{main_url}..下载文件....")
    try:
        for j in josn_list:
            url = main_url + j
            path = _DATA_PATH / j
            logger.info(f"正在下载{j}....")
            for _ in range(3):
                try:
                    data = (await AsyncHttpx.get(url)).json()
                    async with aiofiles.open(path, "w") as wf:
                        await wf.write(json.dumps(data))
                    logger.info(f"{j}下载完成....")
                    break
                except TimeoutError:
                    pass
            else:
                logger.error(f"下载文件 {url} 下载超时.. Path：{path}")
        return data
    except Exception as e:
        logger.error(f"下载文件 {url} 未知错误 {type(e)}：{e}.. Path：{path}")
    return False


async def download_bwiki_shipalias():
    """
    
    从 https://wiki.biligame.com/blhx/舰娘图鉴 上获取所有带和谐名的舰娘名称和和谐名添加到alias.json
    
    """
    url = "https://wiki.biligame.com/blhx/%E8%88%B0%E5%A8%98%E5%9B%BE%E9%89%B4"
    text = (await AsyncHttpx.get(url)).text
    soup = BeautifulSoup(text, "lxml")
    type_lst = soup.find("div", {
        "class": "resp-tabs-container"
    }).find_all("div", {"class": "resp-tab-content"})

    names = {}
    path = _DATA_PATH / "alias.json"

    logger.info(f"获取alias.json....")
    for char_lst in type_lst:
        try:
            contents = char_lst.find("table").find("tbody").contents[-1].find(
                "td").contents
        except AttributeError:
            continue
        for char in contents[1:]:
            try:
                char = char.find("div").contents[-1].find("a")
                name = ("".join(char["title"].split()))
                try:
                    alias = ("".join(char.find("span").text.split()))
                    if alias != name:
                        names.update({name: alias})
                except AttributeError:
                    continue
            except AttributeError:
                continue
    async with aiofiles.open(path, "wb") as wf:
        await wf.write(
            json.dumps(names, indent=2, ensure_ascii=False).encode())
    return path


async def update_name_dict():
    """
    
    从 alias.json 和 ships.json 中获取数据生成 names.json
    
    """

    ships = {}

    # 判断文件是否存在，不存在的话就不进行读取
    try:
        async with aiofiles.open(_DATA_PATH / "names.json",
                                 "r",
                                 encoding="utf-8") as fp:
            ships = json.loads(await fp.read())
    except:
        pass
    data = await download_azurapi_data()
    if data:
        try:
            alias = await download_bwiki_shipalias()
        except:
            return "bwiki舰船名称拉取错误，注意插件更新"
    else:
        logger.error(f"更新数据文件错误")
        return f"更新数据文件错误，请前往 https://github.com/AzurAPI/azurapi-js-setup 手动更新"
    logger.info(f"生成names.json....")
    for item in data:
        if item["id"] in ships.keys():
            continue
        ships[item["id"]] = [
            item["names"]["cn"], item["names"]["jp"], item["names"]["kr"],
            item["names"]["en"]
        ]
        try:
            alias_cn = alias[item["names"]["cn"]]
            ships[item["id"]].insert(1, alias_cn)
        except:
            pass
    async with aiofiles.open(_DATA_PATH / "names.json", "w",
                             encoding="utf-8") as fp:
        await fp.write(json.dumps(ships, indent=2, ensure_ascii=False))
