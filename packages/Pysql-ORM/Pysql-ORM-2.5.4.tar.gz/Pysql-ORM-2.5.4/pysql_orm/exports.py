# -*- coding: utf-8 -*-
"""
#/*
##; Copyright (c) 2010-2021, Armin Ronacher(BSD-3-Clause)
##; All rights reserved.
##; 
##; @@@Origin: https://github.com/pallets-eco/flask-sqlalchemy/blob/2.5.1/flask_sqlalchemy/__init__.py
##; 
##; This module is part of SQLAlchemy and is released under
##; the BSD-3-Clause License: https://opensource.org/license/bsd-3-clause
##; details as below:
#*
#* Redistribution and use in source and binary forms, with or without
#* modification, are permitted provided that the following conditions are met:
#*
#* 1. Redistributions of source code must retain the above copyright notice, this
#*    list of conditions and the following disclaimer.
#*
#* 2. Redistributions in binary form must reproduce the above copyright notice,
#*    this list of conditions and the following disclaimer in the documentation
#*    and/or other materials provided with the distribution.
#*
#* 3. Neither the name of the copyright holder nor the names of its
#*    contributors may be used to endorse or promote products derived from
#*    this software without specific prior written permission.
#*
#* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#* FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#* DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#* SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#* CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#* OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#* OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#*/
"""

from __future__ import absolute_import

import os
import warnings
from threading import Lock

import sqlalchemy
import flask
from sqlalchemy import orm
from sqlalchemy.engine.url import make_url
from sqlalchemy.engine import Connection
from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.orm.session import Session as SessionBase

from .model import DefaultMeta, DeclarativeMeta, declarative_base
from .model import Model
from ._compat import itervalues, string_types, _ident_func
from ._adapt import AppCfgAdaptor, FSADeprecationWarning
from . import utils
from . import _sa_help as sa_help

warnings.simplefilter('always', FSADeprecationWarning)


class SignallingSession(SessionBase):
    """The signalling session is the default session that Flask-SQLAlchemy
    uses.  It extends the default session system with bind selection and
    modification tracking.

    If you want to use a different session you can override the
    :meth:`SQLAlchemy.create_session` function.

    .. versionadded:: 2.0

    .. versionadded:: 2.1
        The `binds` option was added, which allows a session to be joined
        to an external transaction.
    """

    def __init__(self, db: AppCfgAdaptor, autocommit=False, autoflush=True,
                 bind=None, binds=None, **options
                 ):
        #: The application that this session belongs to.
        self.db = db  # type: (SQLAlchemy, AppCfgAdaptor)
        self._app = None
        # track_modifications = app.config['SQLALCHEMY_TRACK_MODIFICATIONS']        
        # bind = options.pop('bind', None) or db.engine
        # binds = options.pop('binds', db.get_binds(app))
        if db.cfg_option("SQLALCHEMY_TRACK_MODIFICATIONS", False):
            sa_help._SessionSignalEvents.register(self)

        SessionBase.__init__(
            self, autocommit=autocommit, autoflush=autoflush,
            bind=bind, binds=binds, **options
        )

    @property
    def app(self):
        if self._app is None:
            self._app = self.db.get_app(self._app)
        return self._app

    def get_bind(self, mapper=None, clause=None):
        """Return the engine or connection for a given model or
        table, using the ``__bind_key__`` if it is set.
        """
        # mapper is None if someone tries to just get a connection
        if mapper is not None:
            try:
                # SA >= 1.3
                persist_selectable = mapper.persist_selectable
            except AttributeError:
                # SA < 1.3
                persist_selectable = mapper.mapped_table

            info = getattr(persist_selectable, 'info', {})
            bind_key = info.get('bind_key')
            if bind_key is not None and isinstance(self.db, SQLAlchemy):
                return self.db.get_engine(bind=bind_key)
        return SessionBase.get_bind(self, mapper, clause)  # type: Connection 


class _QueryProperty(object):
    def __init__(self, sa):
        self.sa = sa

    def __get__(self, obj, type):
        try:
            mapper = orm.class_mapper(type)
            if mapper:
                return type.query_class(mapper, session=self.sa.session())
        except UnmappedClassError:
            return None


class _EngineConnector(AppCfgAdaptor):
    def __init__(self, sa, app=None, bind=None, app_config=None):
        self._sa = sa
        self._app = app
        self._app_config = app_config
        self._bind_key = bind
        self._ori_db_uri = self.get_uri()
        self._ori_db_echo = False
        ###; lazy loads, dynamic modify
        self._engine = None
        self._connected_for = None
        self._lock = Lock()
        if self.check_debug():
            self.get_engine = self._check_engine
        else:
            self.get_engine = self._fetch_engine


    def __repr__(self):
        return f"<_EngineConnector:{self._connected_for}>"

    def get_uri(self):
        if self._bind_key is None:
            return self.cfg_option('SQLALCHEMY_DATABASE_URI')
        binds = self.cfg_option('SQLALCHEMY_BINDS', default_value=())
        assert self._bind_key in binds, \
            'Bind %r is not specified.  Set it in the SQLALCHEMY_BINDS ' \
            'configuration variable' % self._bind_key
        return binds[self._bind_key]

    def _fetch_engine(self):
        ##; better performance, Origin Flask-Sqlalchemy
        with self._lock:
            if self._engine is None:
                sa_url = make_url(self._ori_db_uri)
                sa_url, options = self.get_engine_options(sa_url, self._ori_db_echo)
                self._engine = self._sa.create_engine(sa_url, options)
                self._connected_for = (self._ori_db_uri, self._ori_db_echo)
            return self._engine

    def _check_engine(self):
        ##; lower performance, Origin Flask-Sqlalchemy
        with self._lock:
            uri = self.get_uri()
            echo = self.cfg_option('SQLALCHEMY_ECHO', default_value=False)
            if (uri, echo) == self._connected_for:
                return self._engine

            sa_url = make_url(uri)
            sa_url, options = self.get_engine_options(sa_url, echo)
            self._engine = rv = self._sa.create_engine(sa_url, options)

            if self._app is not None:
                if self.check_debug():
                    app_imp_name = getattr(
                        self._app, "import_name",
                        self.cfg_option("APP_IMPORT_NAME", default_value=str(self._app))
                    )
                    sa_help._EngineDebuggingSignalEvents(
                        self._engine,
                        app_imp_name,
                    ).register()

            self._connected_for = (uri, echo)

            return rv

    def get_engine_options(self, sa_url, echo):
        options = {}

        options = self._sa.apply_pool_defaults(self._app, options)
        sa_url, options = self._sa.apply_driver_hacks(self._app, sa_url, options)

        if echo:
            options['echo'] = echo

        # Give the config options set by a developer explicitly priority
        # over decisions FSA makes.
        opts = self.cfg_option('SQLALCHEMY_ENGINE_OPTIONS', default_value={})
        options.update(opts)

        # Give options set in SQLAlchemy.__init__() ultimate priority
        options.update(self._sa._engine_options)

        return sa_url, options


class _SQLAlchemyState(object):
    """Remembers configuration for the (db, app) tuple."""

    def __init__(self, db):
        self.db = db  # type: SQLAlchemy
        self.connectors = {}


class SQLAlchemy(AppCfgAdaptor):
    """This class is used to control the SQLAlchemy integration to one
    or more Flask applications.  Depending on how you initialize the
    object it is usable right away or will attach as needed to a
    Flask application.

    There are two usage modes which work very similarly.  One is binding
    the instance to a very specific Flask application::

        app = Flask(__name__)
        db = SQLAlchemy(app)

    The second possibility is to create the object once and configure the
    application later to support it::

        db = SQLAlchemy()

        def create_app():
            app = Flask(__name__)
            db.init_app(app)
            return app

    The difference between the two is that in the first case methods like
    :meth:`create_all` and :meth:`drop_all` will work all the time but in
    the second case a :meth:`flask.Flask.app_context` has to exist.

    By default Flask-SQLAlchemy will apply some backend-specific settings
    to improve your experience with them.

    As of SQLAlchemy 0.6 SQLAlchemy
    will probe the library for native unicode support.  If it detects
    unicode it will let the library handle that, otherwise do that itself.
    Sometimes this detection can fail in which case you might want to set
    ``use_native_unicode`` (or the ``SQLALCHEMY_NATIVE_UNICODE`` configuration
    key) to ``False``.  Note that the configuration key overrides the
    value you pass to the constructor.  Direct support for ``use_native_unicode``
    and SQLALCHEMY_NATIVE_UNICODE are deprecated as of v2.4 and will be removed
    in v3.0.  ``engine_options`` and ``SQLALCHEMY_ENGINE_OPTIONS`` may be used
    instead.

    This class also provides access to all the SQLAlchemy functions and classes
    from the :mod:`sqlalchemy` and :mod:`sqlalchemy.orm` modules.  So you can
    declare models like this::

        class User(db.Model):
            username = db.Column(db.String(80), unique=True)
            pw_hash = db.Column(db.String(80))

    You can still use :mod:`sqlalchemy` and :mod:`sqlalchemy.orm` directly, but
    note that Flask-SQLAlchemy customizations are available only through an
    instance of this :class:`SQLAlchemy` class.  Query classes default to
    :class:`BaseQuery` for `db.Query`, `db.Model.query_class`, and the default
    query_class for `db.relationship` and `db.backref`.  If you use these
    interfaces through :mod:`sqlalchemy` and :mod:`sqlalchemy.orm` directly,
    the default query class will be that of :mod:`sqlalchemy`.

    .. admonition:: Check types carefully

       Don't perform type or `isinstance` checks against `db.Table`, which
       emulates `Table` behavior but is not a class. `db.Table` exposes the
       `Table` interface, but is a function which allows omission of metadata.

    The ``session_options`` parameter, if provided, is a dict of parameters
    to be passed to the session constructor.  See :class:`~sqlalchemy.orm.session.Session`
    for the standard options.

    The ``engine_options`` parameter, if provided, is a dict of parameters
    to be passed to create engine.  See :func:`~sqlalchemy.create_engine`
    for the standard options.  The values given here will be merged with and
    override anything set in the ``'SQLALCHEMY_ENGINE_OPTIONS'`` config
    variable or othewise set by this library.

    .. versionadded:: 0.10
       The `session_options` parameter was added.

    .. versionadded:: 0.16
       `scopefunc` is now accepted on `session_options`. It allows specifying
        a custom function which will define the SQLAlchemy session's scoping.

    .. versionadded:: 2.1
       The `metadata` parameter was added. This allows for setting custom
       naming conventions among other, non-trivial things.

       The `query_class` parameter was added, to allow customisation
       of the query class, in place of the default of :class:`BaseQuery`.

       The `model_class` parameter was added, which allows a custom model
       class to be used in place of :class:`Model`.

    .. versionchanged:: 2.1
       Utilise the same query class across `session`, `Model.query` and `Query`.

    .. versionadded:: 2.4
       The `engine_options` parameter was added.

    .. versionchanged:: 2.4
       The `use_native_unicode` parameter was deprecated.

    .. versionchanged:: 2.4.3
        ``COMMIT_ON_TEARDOWN`` is deprecated and will be removed in
        version 3.1. Call ``db.session.commit()`` directly instead.

    ========================================================
    ##; flask-sqlalchemy==2.5.1 >>> PysqlOrm==2.5.3 
    ========================================================    
    .. versionchanged:: 2.5.3
        query_class change defaults from class:`BaseQuery(FsaQuery)` to `orm.Query`
        lazyload with default as None 
        
    """

    #: Default query class used by :attr:`Model.query` and other queries.
    #: Customize this by passing ``query_class`` to :func:`SQLAlchemy`.
    Query = None

    def __init__(self, app=None, use_native_unicode=True, session_options=None,
                 metadata=None, query_class=None, model_class=Model,
                 engine_options=None, config=None, _app_framework="flask",
                 ):
        ##; dirty for Decoupling failed on Query-Model-session 
        if query_class is None:
            if app is None:
                query_class = orm.Query
                _app_framework = ""
            elif _app_framework == "flask":
                from .exts._flask import FsaQuery
                query_class = FsaQuery
            else:
                ##; Defaults to :class:`orm.Query` 
                query_class = orm.Query

        self._conn_state = None
        self._app = app
        self._app_config = config
        self._app_framework = _app_framework
        self._model_class = model_class
        self._engine_options = engine_options or {}
        self._engine_lock = Lock()

        self.use_native_unicode = use_native_unicode
        self.Query = query_class
        self.Model = self.make_declarative_base(model_class, metadata)
        self.session = self.create_scoped_session(session_options)
            
        sa_help._include_sqlalchemy(self, query_class)
        if app is not None:
            self.init_app(app)
        self.init_config()

    @property
    def metadata(self):
        """The metadata associated with ``db.Model``."""

        return self.Model.metadata

    def create_scoped_session(self, options=None):
        """Create a :class:`~sqlalchemy.orm.scoping.scoped_session`
        on the factory from :meth:`create_session`.

        An extra key ``'scopefunc'`` can be set on the ``options`` dict to
        specify a custom scope function.  If it's not provided, Flask's app
        context stack identity is used. This will ensure that sessions are
        created and removed with the request/response cycle, and should be fine
        in most cases.

        :param options: dict of keyword arguments passed to session class  in
            ``create_session``
        """

        if options is None:
            options = {}

        scopefunc = options.pop('scopefunc', _ident_func)
        options.setdefault('query_cls', self.Query)
        return orm.scoped_session(
            self.create_session(options), scopefunc=scopefunc
        )

    def create_session(self, options):
        """Create the session factory used by :meth:`create_scoped_session`.

        The factory **must** return an object that SQLAlchemy recognizes as a session,
        or registering session events may raise an exception.

        Valid factories include a :class:`~sqlalchemy.orm.session.Session`
        class or a :class:`~sqlalchemy.orm.session.sessionmaker`.

        The default implementation creates a ``sessionmaker`` for :class:`SignallingSession`.

        :param options: dict of keyword arguments passed to session class
        """
        bind = options.pop('bind', None) or self.engine
        binds = options.pop('binds', self.get_binds(self._app))
        return orm.sessionmaker(
            class_=SignallingSession, db=self,
            app=self._app, bind=bind, binds=binds,
            **options
        )

    def make_declarative_base(self, model, metadata=None):
        """Creates the declarative base that all models will inherit from.

        :param model: base model class (or a tuple of base classes) to pass
            to :func:`~sqlalchemy.ext.declarative.declarative_base`. Or a class
            returned from ``declarative_base``, in which case a new base class
            is not created.
        :param metadata: :class:`~sqlalchemy.MetaData` instance to use, or
            none to use SQLAlchemy's default.

        .. versionchanged 2.3.0::
            ``model`` can be an existing declarative base in order to support
            complex customization such as changing the metaclass.
        """
        if not isinstance(model, DeclarativeMeta):
            model = declarative_base(
                cls=model,
                name='Model',
                metadata=metadata,
                metaclass=DefaultMeta
            )

        # if user passed in a declarative base and a metaclass for some reason,
        # make sure the base uses the metaclass
        if metadata is not None and model.metadata is not metadata:
            model.metadata = metadata

        if not getattr(model, 'query_class', None):
            model.query_class = self.Query

        model.query = _QueryProperty(self)
        return model


    def init_config(self):
        cfg = self.make_config(self.app_config)
        ##; Deprecation warnings for config keys that should be replaced by SQLALCHEMY_ENGINE_OPTIONS.
        utils.engine_config_warning(cfg, '3.0', 'SQLALCHEMY_POOL_SIZE', 'pool_size')
        utils.engine_config_warning(cfg, '3.0', 'SQLALCHEMY_POOL_TIMEOUT', 'pool_timeout')
        utils.engine_config_warning(cfg, '3.0', 'SQLALCHEMY_POOL_RECYCLE', 'pool_recycle')
        utils.engine_config_warning(cfg, '3.0', 'SQLALCHEMY_MAX_OVERFLOW', 'max_overflow')
        return cfg


    def __init_app(self, app, cfg=None):
        """This callback can be used to initialize an application for the
        use with this database setup.  Never use a database in the context
        of an application not initialized that way or connections will
        leak.
        """
        if cfg is None:
            try:
                cfg = app.config  # type: dict
                if not self.app_config:
                    self.app_config = cfg
                else:
                    self.app_config.update(cfg)
            except AttributeError as e:
                if not self.app_config:
                    cfg = self.app_config
                    warnings.warn(
                        f'[{self}]: "app.config" is not set! '
                        f'Defaulting "app.config = {cfg}"'
                    )

        if (
            'SQLALCHEMY_DATABASE_URI' not in cfg and
            'SQLALCHEMY_BINDS' not in cfg
        ):
            warnings.warn(
                'Neither SQLALCHEMY_DATABASE_URI nor SQLALCHEMY_BINDS is set. '
                'Defaulting SQLALCHEMY_DATABASE_URI to "sqlite:///:memory:".'
            )

        ## app.extensions['sqlalchemy'] = _SQLAlchemyState(self)
        exts = getattr(app, "extensions", {})
        exts['sqlalchemy'] = self._conn_state
        app.extensions = exts

    def init_app(self, app, cfg=None, app_framework="flask"):
        ##; TODO@NICO: app_framework use enum-strings
        if app_framework == "flask" or isinstance(app, flask.Flask):
            self._app_framework = "flask"
            self.init_flask_app(app, cfg)
        elif app is not None:
            warnings.warn(f"Unknown APP({app}): {type(app)} ???")
            self.__init_app(app, cfg)

    def init_flask_app(self, app, cfg=None):
        self.__init_app(app, cfg=cfg)

        @app.teardown_appcontext
        def shutdown_session(response_or_exc):
            if self.cfg_option('SQLALCHEMY_COMMIT_ON_TEARDOWN'):
                warnings.warn(
                    "'COMMIT_ON_TEARDOWN' is deprecated and will be"
                    " removed in version 3.1. Call"
                    " 'db.session.commit()'` directly instead.",
                    DeprecationWarning,
                )

                if response_or_exc is None:
                    self.session.commit()

            self.session.remove()
            return response_or_exc

    def apply_pool_defaults(self, app, options):
        """
        .. versionchanged:: 2.5
            Returns the ``options`` dict, for consistency with
            :meth:`apply_driver_hacks`.
        """

        def _setdefault(optionkey, configkey):
            value = self.cfg_option(configkey)
            if value is not None:
                options[optionkey] = value

        _setdefault('pool_size', 'SQLALCHEMY_POOL_SIZE')
        _setdefault('pool_timeout', 'SQLALCHEMY_POOL_TIMEOUT')
        _setdefault('pool_recycle', 'SQLALCHEMY_POOL_RECYCLE')
        _setdefault('max_overflow', 'SQLALCHEMY_MAX_OVERFLOW')
        return options

    def apply_driver_hacks(self, app, sa_url, options):
        """This method is called before engine creation and used to inject
        driver specific hacks into the options.  The `options` parameter is
        a dictionary of keyword arguments that will then be used to call
        the :func:`sqlalchemy.create_engine` function.

        The default implementation provides some saner defaults for things
        like pool sizes for MySQL and sqlite.  Also it injects the setting of
        `SQLALCHEMY_NATIVE_UNICODE`.

        .. versionchanged:: 2.5
            Returns ``(sa_url, options)``. SQLAlchemy 1.4 made the URL
            immutable, so any changes to it must now be passed back up
            to the original caller.
        """
        if sa_url.drivername.startswith('mysql'):
            sa_url = sa_help._sa_url_query_setdefault(sa_url, charset="utf8")

            if sa_url.drivername != 'mysql+gaerdbms':
                options.setdefault('pool_size', 10)
                options.setdefault('pool_recycle', 7200)
        elif sa_url.drivername == 'sqlite':
            pool_size = options.get('pool_size')
            detected_in_memory = False
            if sa_url.database in (None, '', ':memory:'):
                detected_in_memory = True
                from sqlalchemy.pool import StaticPool
                options['poolclass'] = StaticPool
                if 'connect_args' not in options:
                    options['connect_args'] = {}
                options['connect_args']['check_same_thread'] = False

                # we go to memory and the pool size was explicitly set
                # to 0 which is fail.  Let the user know that
                if pool_size == 0:
                    raise RuntimeError('SQLite in memory database with an '
                                       'empty queue not possible due to data '
                                       'loss.'
                                       )
            # if pool size is None or explicitly set to 0 we assume the
            # user did not want a queue for this sqlite connection and
            # hook in the null pool.
            elif not pool_size:
                from sqlalchemy.pool import NullPool
                options['poolclass'] = NullPool

            # if it's not an in memory database we make the path absolute.
            if not detected_in_memory:
                sa_url = sa_help._sa_url_set(
                    sa_url, database=os.path.join(app.root_path, sa_url.database)
                )

        unu = self.cfg_option('SQLALCHEMY_NATIVE_UNICODE')
        if unu is None:
            unu = self.use_native_unicode
        if not unu:
            options['use_native_unicode'] = False

        if self.cfg_option('SQLALCHEMY_NATIVE_UNICODE') is not None:
            warnings.warn(
                "The 'SQLALCHEMY_NATIVE_UNICODE' config option is deprecated and will be removed in"
                " v3.0.  Use 'SQLALCHEMY_ENGINE_OPTIONS' instead.",
                DeprecationWarning
            )
        if not self.use_native_unicode:
            warnings.warn(
                "'use_native_unicode' is deprecated and will be removed in v3.0."
                "  Use the 'engine_options' parameter instead.",
                DeprecationWarning
            )

        return sa_url, options

    @property
    def engine(self):
        """Gives access to the engine.  If the database configuration is bound
        to a specific application (initialized with an application) this will
        always return a database connection.  If however the current application
        is used this might raise a :exc:`RuntimeError` if no application is
        active at the moment.
        """
        return self.get_engine()

    def make_connector(self, app=None, bind=None):
        """Creates the connector for a given state and bind."""
        app_ = self.get_app(app, nullable=True)
        app_config = self.app_config
        return _EngineConnector(self, app=app_, bind=bind, app_config=app_config)


    def get_state(self, app=None):
        app = self.get_app(app, nullable=True)
        if app is not None:
            """Gets the state for the application"""
            assert 'sqlalchemy' in app.extensions, \
                'The sqlalchemy extension was not registered to the current ' \
                'application.  Please make sure to call init_app() first.'
            return app.extensions['sqlalchemy']  # type: _SQLAlchemyState
        if not self.app_config:
            warnings.warn(
                "SQLAlchemy(app=None, app=config=None),"
                "you should init_app() or set app_config before "
            )

        elif not self._conn_state:
            self._conn_state = _SQLAlchemyState(self)
        return self._conn_state


    def get_engine(self, app=None, bind=None):
        """Returns a specific engine."""
        state = self.get_state(app)  # type: _SQLAlchemyState

        with self._engine_lock:
            connector = state.connectors.get(bind)

            if connector is None:
                connector = self.make_connector(app, bind)
                state.connectors[bind] = connector

            return connector.get_engine()  # type: _EngineConnector


    def create_engine(self, sa_url, engine_opts):
        """
            Override this method to have final say over how the SQLAlchemy engine
            is created.

            In most cases, you will want to use ``'SQLALCHEMY_ENGINE_OPTIONS'``
            config variable or set ``engine_options`` for :func:`SQLAlchemy`.
        """
        return sqlalchemy.create_engine(sa_url, **engine_opts)


    def get_app(self, reference_app=None, nullable=False):
        """Helper method that implements the logic to look up an
        application."""

        if reference_app is not None:
            return reference_app

        if flask.has_app_context():
            return flask.current_app  # type: flask.Flask

        if self._app is not None:
            return self._app

        if nullable:
            return None

        raise RuntimeError(
            'No application found. Either work inside a view function or push'
            ' an application context. See'
            ' http://flask-sqlalchemy.pocoo.org/contexts/.'
        )

    def get_tables_for_bind(self, bind=None):
        """Returns a list of all tables relevant for a bind."""
        result = []
        for table in itervalues(self.Model.metadata.tables):
            if table.info.get('bind_key') == bind:
                result.append(table)
        return result

    def get_binds(self, app=None):
        """Returns a dictionary with a table->engine mapping.

        This is suitable for use of sessionmaker(binds=db.get_binds(app)).
        """
        app = self.get_app(app, nullable=True)
        binds = [None] + list(self.cfg_option('SQLALCHEMY_BINDS', default_value=()))
        retval = {}
        for bind in binds:
            engine = self.get_engine(app, bind)
            tables = self.get_tables_for_bind(bind)
            retval.update(dict((table, engine) for table in tables))
        return retval

    def _execute_for_all_tables(self, app, bind, operation, skip_tables=False):
        app = self.get_app(app, nullable=True)

        if bind == '__all__':
            binds = [None] + list(self.cfg_option('SQLALCHEMY_BINDS', default_value=()))
        elif isinstance(bind, string_types) or bind is None:
            binds = [bind]
        else:
            binds = bind

        for bind in binds:
            extra = {}
            if not skip_tables:
                tables = self.get_tables_for_bind(bind)
                extra['tables'] = tables
            op = getattr(self.Model.metadata, operation)
            op(bind=self.get_engine(app, bind), **extra)

    def create_all(self, bind='__all__', app=None):
        """Creates all tables.

        .. versionchanged:: 0.12
           Parameters were added
        """
        self._execute_for_all_tables(app, bind, 'create_all')

    def drop_all(self, bind='__all__', app=None):
        """Drops all tables.

        .. versionchanged:: 0.12
           Parameters were added
        """
        self._execute_for_all_tables(app, bind, 'drop_all')

    def reflect(self, bind='__all__', app=None):
        """Reflects tables from the database.

        .. versionchanged:: 0.12
           Parameters were added
        """
        self._execute_for_all_tables(app, bind, 'reflect', skip_tables=True)

    def __repr__(self):
        s = super(SQLAlchemy, self).__repr__()
        return f"{s}:{self.get_uri(safety_wrap=self.check_debug())}"

    @property
    def app(self):
        return self.get_app(self._app)
