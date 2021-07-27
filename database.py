from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from Language import Language

engine = create_engine("sqlite:////tmp/data.db")
Base = declarative_base(engine)
metadata = Base.metadata
Session = sessionmaker(bind=engine)
session = Session()


class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    guild_id = Column(Integer, ForeignKey("guilds.id"), nullable=False)
    language = Column(Enum(Language), nullable=True)


class ChannelGroupChannel(Base):
    __tablename__ = "channel_group_channels"
    channel_group_id = Column(Integer, ForeignKey("channel_groups.id"), primary_key=True, nullable=False)
    channel_id = Column(Integer, ForeignKey("channels.id"), primary_key=True, nullable=False)


class ChannelGroup(Base):
    __tablename__ = "channel_groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(Integer, ForeignKey("guilds.id"), nullable=False)
    name = Column(String)

    channels = relationship("Channel", backref="groups", secondary="channel_group_channels", cascade="all, delete")


class Guild(Base):
    __tablename__ = "guilds"
    id = Column(Integer, primary_key=True, nullable=False)
    prefix = Column(String, nullable=False, default="+")

    channels = relationship("Channel", backref="guild", cascade="all, delete-orphan")
    channel_groups = relationship("ChannelGroup", backref="guild", cascade="all, delete-orphan")


Base.metadata.create_all(bind=engine)
session.commit()
