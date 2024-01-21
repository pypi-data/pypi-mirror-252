import importlib
import os

from hebill_websites_core import websites_core
from hebill_websites_core.__constants__ import *


class website_core:
    # 根目录路径
    _name: str = None
    # 根目录设置文件路径，不可更改，里面需要有 settings 字典变量
    settings_default = {}
    settings = {}

    def __init__(self, websites: websites_core, name: str):
        self._websites_core = websites
        self._name = name
        try:
            _sn = importlib.import_module(self._websites_core.websites_dirname + "." + self.name + ".__settings__")
        except ImportError:
            _sn = None
        if _sn is not None and hasattr(_sn, 'settings') and isinstance(_sn.settings, dict):
            self._settings = _sn.settings

    def setting(self, name):
        if name in self.settings:
            return self.settings[name]
        if name in self.settings_default:
            return self.settings_default[name]
        return None

    def _setting_read_include_websites_core(self, name):
        v = self.setting(name)
        if v is not None:
            return v
        return self._websites_core.setting(name)

    # 不可更改属性
    @property
    def name(self) -> str:
        return self._name

    # 设置转换为属性
    @property
    def langauge(self) -> str:
        return self._setting_read_include_websites_core(SN_LANGUAGE)

    # 动态属性
    @property
    def root_path(self) -> str:
        return os.path.join(self._websites_core.websites_dir_path, self.name)
