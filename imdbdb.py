# coding: utf-8
from pathlib import Path
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
import logging


# Global Variables
SQLITE = 'sqlite'

DB_NAME = 'imdb.db'
DB_URL = 'sqlite:///{}'.format(DB_NAME)


Base = declarative_base()
metadata = Base.metadata


t_akas = Table(
    'akas', metadata,
    Column('title_id', String, index=True),
    Column('title', String, index=True),
    Column('region', String),
    Column('language', String),
    Column('types', String),
    Column('attributes', String),
    Column('is_original_title', Integer)
)


t_crew = Table(
    'crew', metadata,
    Column('title_id', String, index=True),
    Column('person_id', String, index=True),
    Column('category', String),
    Column('job', String),
    Column('characters', String)
)


t_episodes = Table(
    'episodes', metadata,
    Column('episode_title_id', Integer, index=True),
    Column('show_title_id', Integer, index=True),
    Column('season_number', Integer),
    Column('eposide_number', Integer)
)


class Person(Base):
    __tablename__ = 'people'

    person_id = Column(String, primary_key=True)
    name = Column(String, index=True)
    born = Column(Integer)
    died = Column(Integer)


class Rating(Base):
    __tablename__ = 'ratings'

    title_id = Column(String, primary_key=True)
    rating = Column(Integer)
    votes = Column(Integer)


class Title(Base):
    __tablename__ = 'titles'

    title_id = Column(String, primary_key=True)
    type = Column(String, index=True)
    primary_title = Column(String, index=True)
    original_title = Column(String, index=True)
    is_adult = Column(Integer)
    premiered = Column(Integer)
    ended = Column(Integer)
    runtime_minutes = Column(Integer)
    genres = Column(String)


class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: DB_URL}

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        if not Path(DB_NAME).exists():
            print(
                'Database "{}" not exists. please run "imdb-sqlite" first'.format(DB_NAME))
            logging.error('Database not exists')
            exit(1)
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            logging.debug(engine_url)
            self.db_engine = create_engine(engine_url)
            logging.debug(self.db_engine)
        else:
            logging.error("DBType is not found in DB_ENGINE")


imdb = MyDatabase(SQLITE, dbname=DB_NAME)
Base.metadata.create_all(imdb.db_engine)
Base.metadata.bind = imdb.db_engine
DBSession = sessionmaker(
    bind=imdb.db_engine, autoflush=False, autocommit=False)
session = DBSession()


imdb_all_search = session.query(Title.title_id,
                                Title.runtime_minutes,
                                Title.type,
                                Title.premiered,
                                t_akas.columns['region'],
                                t_akas.columns['title']
                                ).filter(t_akas.columns['title_id'] == Title.title_id
                                         ).filter(Title.type.in_(['movie', 'video']))

imdb_title = session.query(Title.title_id,
                           Title.primary_title,
                           Title.original_title,
                           Title.premiered,
                           Title.genres)

imdb_title_ru = session.query(t_akas.columns['title']).filter(
    t_akas.columns['language'] == 'RU')
