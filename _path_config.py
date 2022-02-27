from utils.manager import resources_manager
from pathlib import Path
import os

path_ = Path(__file__).parent

# 图片路径
_IMAGE_PATH = path_ / "resources" / "image"
# 语音路径
# RECORD_PATH = Path() / "resources" / "record"
# 字体路径
_FONT_PATH = path_ / "resources" / "font"
# 数据路径
_DATA_PATH = path_ / "resources" / "data"
# 临时数据路径
_TEMP_PATH = path_ / "resources" / "temp"


def load_path():
    _IMAGE_PATH.mkdir(parents=True, exist_ok=True)
    # _RECORD_PATH.mkdir(parents=True, exist_ok=True)
    _FONT_PATH.mkdir(parents=True, exist_ok=True)
    _DATA_PATH.mkdir(parents=True, exist_ok=True)
    _TEMP_PATH.mkdir(parents=True, exist_ok=True)
    resources_manager.add_temp_dir(_TEMP_PATH)

load_path()



