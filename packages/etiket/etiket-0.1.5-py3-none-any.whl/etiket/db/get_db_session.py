from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from starlette.requests import Request
from etiket.settings import settings

from typing import Generator

class database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(database, cls).__new__(cls)
            cls.engine = create_engine(
                settings.db_url,
                max_overflow=20,
                pool_size=20
            )
            cls.session_factory = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        return cls._instance

    @classmethod
    def get_engine(cls):
        if cls._instance is None:
            cls()
        return cls._instance.engine
    
    @classmethod
    def get_session_factory(cls):
        if cls._instance is None:
            cls()
        return cls._instance.session_factory
   
def get_db_session(request: Request) -> Generator[Session, None, None]:
    session = request.app.state.db_session_factory()
    
    try:
        # TODO move this to default time zones
        session.execute(text("SET TIME ZONE 'UTC';"))
        yield session
    finally:
        session.commit()
        session.close()
        
def get_db_session_raw() -> Session:
    session_factory =  database.get_session_factory()
    return session_factory()

def get_scoped_session_raw() -> Session:
    session_factory =  database.get_session_factory()
    return scoped_session(session_factory())