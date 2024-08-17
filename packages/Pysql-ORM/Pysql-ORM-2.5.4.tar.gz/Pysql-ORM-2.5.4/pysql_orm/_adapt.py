import types
import warnings


class FSADeprecationWarning(DeprecationWarning):
    pass


class _AdaptorMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        if cls is not AppCfgAdaptor:
            AppCfgAdaptor.__init__(obj, *args, **kwargs)
            cls.__init__(obj, *args, **kwargs)
        return obj


class AppCfgAdaptor(metaclass=_AdaptorMeta):
    _refered_cfg = {}
    _app_config = None
    _app = None

    def __init__(self, *args, **kwargs):
        self._ext_args = args
        self._ext_kwargs = kwargs
        self._refered_cfg = {}

    def __str__(self):
        return f"<AppCfgAdaptor: {self.__class__.__name__}>"

    def __repr__(self):
        if self.app_config:
            return f"<{self.__class__.__name__}(app={str(self._app)}, app_config={type(self.app_config)})> "
        else:
            return f"<{self.__class__.__name__}(app={str(self._app)}, app_config={self.app_config})>"

    @property
    def app_config(self):
        cfg = getattr(self, "_app_config", None)
        # return type: dict 
        if cfg and isinstance(cfg, dict):
            return cfg
        app = getattr(self, "_app", None)
        if app is not None:
            cfg = getattr(app, "config", {})
            if not isinstance(cfg, dict):
                warnings.warn(
                    f'{self}: self._app.config is not A Dict, recv {type(cfg)},'
                    f'it make raise error if use self.cfg_opotion, '
                    f'suggest to use `flask.config.Config` to convert it.'
                )
            self._app_config = cfg
        return self._app_config

    @app_config.setter
    def app_config(self, value: dict):
        self._app_config = value

    def check_debug(self):
        if not isinstance(self.app_config, dict):
            return False
        if self.app_config.get("DEBUG", False):
            return True
        rq = self.app_config.get('SQLALCHEMY_RECORD_QUERIES', None)
        if rq is not None:
            return bool(rq)
        return self.app_config.get('TESTING', False)

    def cfg_option(self, key, default_value=None, nullable=True, decode_func=None, **kwargs):
        val = self.app_config.get(key)
        if val is None:
            if self.check_debug():
                warnings.warn(f'{self}: use config({key}), default_value="{default_value}"')
            if not nullable and default_value is None:
                raise AttributeError(f'{self}: config({key}) is required!')
            val = default_value
        elif callable(decode_func):
            val = decode_func(val)
        self._refered_cfg[key] = val
        return val

    def get_uri(self, default_value="", nullable=True, safety_wrap=False, **kwargs):
        m = self.cfg_option('SQLALCHEMY_DATABASE_URI', default_value, nullable=nullable, **kwargs)
        if safety_wrap and isinstance(m, str):
            m = m.split("@", 1)[-1]
        return m

    @classmethod
    def make_config(cls, cfg: dict):
        ##; @SQLALCHEMY_DATABASE_URI:
        ###; "mysql+mysqldb://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8mb4"  
        ###; "sqlite:///{local_db_file}"
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
