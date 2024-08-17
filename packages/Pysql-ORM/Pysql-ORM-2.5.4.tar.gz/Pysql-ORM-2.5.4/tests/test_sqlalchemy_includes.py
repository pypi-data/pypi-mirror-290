import sqlalchemy as sa

import pysql_orm as fsa


def test_sqlalchemy_includes():
    """Various SQLAlchemy objects are exposed as attributes."""
    db = fsa.SQLAlchemy()

    assert db.Column == sa.Column

    # The Query object we expose is actually our own subclass.
    assert db.Query == fsa.BaseQuery
