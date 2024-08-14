import importlib.util
from pathlib import Path

DEFAULTS = {
    "STORAGE": {
        "type": "local",
        "path": "./var",
    },
    "TITLE_PROPERTY": "title",
    "LINK_PROPERTY": "link",
    "MHTML_PROPERTY": "mhtml",
    "SERVER_BIND": "0.0.0.0:8001",
}


class Setting:
    def __init__(self, user_settings=None, defaults=None) -> None:
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid pagesaver setting: '%s'" % attr)
        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]
        setattr(self, attr, val)
        return val

    @classmethod
    def from_object(cls, instance, defaults=None):
        user_settings = {
            key: getattr(instance, key)
            for key in dir(instance)
            if not key.startswith("_")
        }
        return cls(user_settings=user_settings, defaults=defaults)

    @classmethod
    def from_pyfile(cls, filename, defaults=None):
        file_path = Path(filename)
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return cls.from_object(module, defaults)


class LazySetting:
    def __init__(self) -> None:
        self._wrapped = None

    def _setup(self):
        config_path = Path("config.py").absolute()  # Todo
        if config_path.exists():
            self._wrapped = Setting.from_pyfile(config_path, defaults=DEFAULTS)
        else:
            self._wrapped = Setting(user_settings={}, defaults=DEFAULTS)

    def __getattr__(self, attr):
        if self._wrapped is None:
            self._setup()
        return getattr(self._wrapped, attr)


pagesaver_settings = LazySetting()
