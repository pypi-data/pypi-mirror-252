from typing import Any, Tuple

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from viavi.fibermark.db_utils.settings import DB_URI, DB_login, DB_name, DB_password


def create_session(db_login: str) -> Tuple[Any, Session]:
    engine = create_engine(db_login)
    session = Session(bind=engine)
    return engine, session


prod_db_engine, prod_db_session = create_session(
    f"mysql+pymysql://{DB_login}:{DB_password}@{DB_URI}/{DB_name}?charset=utf8mb4"
)
