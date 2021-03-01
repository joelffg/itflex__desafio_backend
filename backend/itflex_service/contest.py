import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from itflex.common.tokens import encode
from itflex.config import TOKEN_SECRET
from itflex.testing import create_sqlite_functions
from itflex_firewall.models import SQLBase
from itflex_sdwan.models import SQLBase as Sdwan_SQLBase

from .deps import get_scopes

DB_URL = "sqlite:///:memory:"


@pytest.fixture
def scopes():
    scopes = []

    for scope in get_scopes():
        scopes.append({"name": scope, "read": True, "write": True})

    return scopes


@pytest.fixture
def superuser_token():
    payload = {
        "sub": 0,
        "sub_type": "user",
        "type": "access",
        "superuser": True,
        "scopes": [],
    }
    token_bytes = encode(payload, TOKEN_SECRET, 3000)
    return token_bytes.decode()


@pytest.fixture
def user_token(scopes):
    payload = {
        "sub": 1,
        "sub_type": "user",
        "type": "access",
        "superuser": False,
        "scopes": scopes,
    }
    token_bytes = encode(payload, TOKEN_SECRET, 3000)
    return token_bytes.decode()


@pytest.fixture
def ssl_token():
    payload = {
        "sub": 0,
        "sub_type": "itflex",
        "type": "access",
        "fullname": "User Test",
        "username": "user01",
        "email": "user01@email.com",
        "superuser": True,
        "scopes": [],
    }
    token_bytes = encode(payload, TOKEN_SECRET, 3000)
    return token_bytes.decode()


@pytest.fixture
def db_engine():
    engine = create_engine(DB_URL)
    conn = engine.raw_connection()
    create_sqlite_functions(conn)
    engine.execute("pragma foreign_keys=on")
    yield engine
    engine.dispose()


@pytest.fixture
def db_sessionmaker(db_engine):
    return sessionmaker(bind=db_engine)


@pytest.fixture(autouse=True)
def create_db(db_engine):
    SQLBase.metadata.create_all(db_engine)
    Sdwan_SQLBase.metadata.create_all(db_engine)

