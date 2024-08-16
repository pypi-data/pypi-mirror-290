import warnings


class FSADeprecationWarning(DeprecationWarning):
    pass


class AppCfgAdaptor(object):
    _app_config = None
    _app = None

    def __init__(self, *args, **kwargs):
        self._ext_args = args
        self._ext_kwargs = kwargs
        self._refered_cfg = {}

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        self.__init__(*args, **kwargs)

    def __str__(self):
        return f"<AppCfgAdaptor: {self.__class__.__name__}>"

    def __repr__(self):
        if self.app_config:
            return f"<{self.__class__.__name__}>: app={str(self._app)}, app_config={type(self.app_config)}"
        else:
            return f"<{self.__class__.__name__}>: app={str(self._app)}, app_config is not ready!"

    @property
    def app_config(self):
        cfg = getattr(self, "_app_config", None)
        # return type: dict 
        if cfg and isinstance(cfg, dict):
            return cfg
        app = getattr(self, "_app", None)
        if app is not None:
            cfg = getattr(app, "config", {})
            self._app_config = cfg
        return self._app_config

    @app_config.setter
    def app_config(self, value: dict):
        self._app_config = value

    def cfg_option(self, key, default_value=None, nullable=True, decode_func=None):
        val = self.app_config.get(key)
        if val is None:
            warnings.warn(f'{self} use config({key}), default_value="{default_value}"')
            if not nullable and default_value is None:
                raise AttributeError(f'{self} config({key}) is required!')
            val = default_value
        elif callable(decode_func):
            val = decode_func(val)
        self._refered_cfg[key] = val
        return val


    @classmethod
    def make_config(cls, cfg: dict):
        cfg.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
        cfg.setdefault('SQLALCHEMY_BINDS', None)
        cfg.setdefault('SQLALCHEMY_NATIVE_UNICODE', None)
        cfg.setdefault('SQLALCHEMY_ECHO', False)
        cfg.setdefault('SQLALCHEMY_RECORD_QUERIES', None)
        cfg.setdefault('SQLALCHEMY_POOL_SIZE', None)
        cfg.setdefault('SQLALCHEMY_POOL_TIMEOUT', None)
        cfg.setdefault('SQLALCHEMY_POOL_RECYCLE', None)
        cfg.setdefault('SQLALCHEMY_MAX_OVERFLOW', None)
        cfg.setdefault('SQLALCHEMY_COMMIT_ON_TEARDOWN', False)
        cfg.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        cfg.setdefault('SQLALCHEMY_ENGINE_OPTIONS', {})
        return cfg

    def check_debug(self):
        if self.cfg_option("DEBUG", default_value=False):
            return True
        rq = self.cfg_option('SQLALCHEMY_RECORD_QUERIES', None)
        if rq is not None:
            return bool(rq)
        return self.cfg_option('TESTING', False)
