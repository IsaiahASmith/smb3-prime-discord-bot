from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/data.db')
Base = declarative_base(engine)
metadata = Base.metadata
Session = sessionmaker(bind=engine)
session = Session()


class Guild(Base):
    __tablename__ = "guilds"
    guild_id = Column(Integer, primary_key=True, nullable=False)
    prefix = Column(String, nullable=False, default="+")

Base.metadata.create_all(bind=engine)
session.commit()