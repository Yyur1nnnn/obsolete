from utils.manager import resources_manager
from pathlib import Path
import os

PATH_ = Path(__file__).parent

# 图片路径
_IMAGE_PATH = PATH_ / "resources" / "image"
# HTML路径
HTML_PATH = PATH_ / "resources" / "html"
# 字体路径
_FONT_PATH = PATH_ / "resources" / "font"
# 数据路径
_DATA_PATH = PATH_ / "resources" / "data"
# 临时数据路径
_TEMP_PATH = PATH_ / "resources" / "temp"


def load_path():
    _IMAGE_PATH.mkdir(parents=True, exist_ok=True)
    HTML_PATH.mkdir(parents=True, exist_ok=True)
    _FONT_PATH.mkdir(parents=True, exist_ok=True)
    _DATA_PATH.mkdir(parents=True, exist_ok=True)
    _TEMP_PATH.mkdir(parents=True, exist_ok=True)
    resources_manager.add_temp_dir(_TEMP_PATH)

load_path()
