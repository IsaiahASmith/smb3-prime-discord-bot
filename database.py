from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:///database.db")
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()