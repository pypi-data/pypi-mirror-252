from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from viavi.fibermark.db_utils.orm import Base
from viavi.fibermark.db_utils.settings import DB_URI, DB_login, DB_password

Created_DB_name = "pls_create_me"
created_db_url = f"mysql+pymysql://{DB_login}:{DB_password}@{DB_URI}/{Created_DB_name}?charset=utf8mb4"

engine = create_engine(created_db_url, echo=True, pool_pre_ping=True)
if not database_exists(engine.url):
    create_database(engine.url)

# Create the tables in the database if it does not exist
Base.metadata.create_all(bind=engine, checkfirst=True)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Commit the changes and close the session
session.commit()
session.close()
