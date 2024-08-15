#!usr/bin/env python3
# -*- coding: utf-8 -*-
from .xiuxian_xiazaishuju import download_xiuxian_data
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent
)
from nonebot import get_driver
from pathlib import Path
from nonebot.log import logger
from nonebot import require
from .config import config as _config  

DRIVER = get_driver()
dir_ = Path(__file__).parent


try:
    NICKNAME: str = list(DRIVER.config.nickname)[0]
except Exception as e:
    logger.info(f"缺少超级用户配置文件，{e}!")
    NICKNAME = 'bot'

try:
    download_xiuxian_data()
except Exception as e:
    logger.info(f"下载配置文件失败，修仙插件无法加载，{e}!")
    raise ImportError


require('nonebot_plugin_apscheduler')
require("xiuxian_boss")
require("xiuxian_bank")
require("xiuxian_sect")
require("xiuxian_info")
require("xiuxian_buff")
require("xiuxian_back")
require("xiuxian_rift")
require("xiuxian_mixelixir")
require("xiuxian_work")
require("xiuxian_base")

__plugin_meta__ = PluginMetadata(
    name='修仙模拟器',
    description='',
    usage=(
        "必死之境机逢仙缘，修仙之路波澜壮阔！\n"
        " 输入 < 修仙帮助 > 获取仙界信息"
    ),
    extra={
        "show": True,
        "priority": 15
    }
)




