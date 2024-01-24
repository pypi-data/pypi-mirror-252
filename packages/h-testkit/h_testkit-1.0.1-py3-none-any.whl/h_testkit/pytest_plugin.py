from os import environ

import pytest

from h_testkit.factoryboy import set_factoryboy_sqlalchemy_session


@pytest.fixture(scope="session")
def db_engine():
    """Return the SQLAlchemy database engine."""
    from sqlalchemy import create_engine

    return create_engine(environ["DATABASE_URL"])


@pytest.fixture(scope="session")
def db_sessionfactory():
    """Return the SQLAlchemy session factory."""
    from sqlalchemy.orm import sessionmaker

    return sessionmaker()


@pytest.fixture
def db_session(db_engine, db_sessionfactory):  # pylint:disable=redefined-outer-name
    """Return the SQLAlchemy database session.

    This returns a session that is wrapped in an external transaction that is
    rolled back after each test, so tests can't make database changes that
    affect later tests.  Even if the test (or the code under test) calls
    session.commit() this won't touch the external transaction.

    This is the same technique as used in SQLAlchemy's own CI:
    https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    db_session = db_sessionfactory(  # pylint:disable=redefined-outer-name
        bind=connection, join_transaction_mode="create_savepoint"
    )
    set_factoryboy_sqlalchemy_session(db_session)

    yield db_session

    db_session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session", autouse=True)
def factory_boy_random_seed():
    """Set factory_boy's random seed.

    Set factory_boy's random seed so that it produces the same random values
     in each run of the tests. See:
     https://factoryboy.readthedocs.io/en/latest/index.html#reproducible-random-values
    """
    import factory.random

    factory.random.reseed_random("hypothesis/h-testkit")
