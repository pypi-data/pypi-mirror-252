from __future__ import annotations

import importlib
import inspect
import os
from hebill_websites_core.__constants__ import *


# 创建websites实例后立即设置相关参数：
# root_path 当前网站根目录路径，为你创建websites实例文件所在目录
class websites_core:

    settings_default = {}
    settings = {}
    websites = {}

    def __init__(self):
        # 获取主动调用文件所在目录，作为网站根目录
        stack = inspect.stack()
        calling_frame = stack[1]
        calling_script_path = calling_frame[1]
        self._root_path = os.path.dirname(os.path.abspath(calling_script_path))
        from hebill_websites_core.websites_core.__settings__ import settings as ss
        self.settings_default = ss
        try:
            sn = importlib.import_module(self.setting_file_name)
        except ImportError:
            sn = None
        if sn is not None and hasattr(sn, self.setting_dirt_name):
            ss = getattr(sn, self.setting_dirt_name)
            if isinstance(ss, dict):
                self.settings = ss

        # 检索根目录下所有
        # self.website_names: list = [d for d in os.listdir(self.root_path)
        #                            if os.path.isdir(os.path.join(self.root_path, d))]

    def setting(self, name):
        if name in self.settings:
            return self.settings[name]
        if name in self.settings_default:
            return self.settings_default[name]
        return None

    # 不可更改属性
    @property
    def root_path(self) -> str:
        return self._root_path

    # 设置转换为属性
    @property
    def language(self) -> str:
        return self.setting(SN_LANGUAGE)

    @property
    def websites_dirname(self) -> str:
        return self.setting(SN_WEBSITES_DIR_NAME)

    @property
    def default_website_name(self) -> str:
        return self.setting(SN_DEFAULT_WEBSITE_NAME)

    @property
    def setting_file_name(self) -> str:
        return self.setting(SN_SETTING_FILE_NAME)

    @property
    def setting_dirt_name(self) -> str:
        return self.setting(SN_SETTING_DIRT_NAME)

    # 动态属性
    @property
    def websites_dir_path(self) -> str:
        return os.path.join(self.root_path, self.websites_dirname)

    from hebill_websites_core.websites_core import website_core

    def junior_website_core(self, name: str = None) -> website_core | None:
        if name is None or name.strip() != "":
            name = self.default_website_name
        if name not in self.websites:
            from hebill_websites_core.websites_core import website_core
            self.websites[name] = website_core(self, name)
        return self.websites[name]
