# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import utils, _adapt, _compat
from ._compat import itervalues, string_types, xrange
from .model import DefaultMeta
from .model import Model
from .extends import SQLAlchemy



version_info = (2, 5, 3)
__version__ = "2.5.3"


##; Copyright (c) 2010-2021, Armin Ronacher(BSD-3-Clause)
_statement_of_refered_packages = {
    "flask-sqlalchemy": dict(
        version="2.5.1",
        RepoUrl="https://github.com/pallets-eco/flask-sqlalchemy/tree/2.5.1",
        License="BSD-3-Clause"
    )
}
