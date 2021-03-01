from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as SessionMaker

from .common.dataclasses import dataclass

__all__ = ["SetupDeps", "setup_deps", "setup_sessionmaker"]

MYSQL_URL = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="password",
    hostname="localhost",
    databasename="mysql",
)


@dataclass
class SetupDeps:
    app: Flask
    sessionmaker: SessionMaker
    socketio: None


def setup_sessionmaker() -> SessionMaker:
    engine = create_engine(MYSQL_URL, pool_recycle=300, pool_size=10)
    sessionmaker = SessionMaker(bind=engine)
    return sessionmaker


def setup_deps(app: Flask = None, socketio=None) -> SetupDeps:
    sessionmaker = setup_sessionmaker()

    return SetupDeps(app=app, sessionmaker=sessionmaker, socketio=socketio)

