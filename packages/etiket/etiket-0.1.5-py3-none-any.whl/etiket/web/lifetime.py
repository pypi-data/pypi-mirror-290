from fastapi import FastAPI

from sqlalchemy import text
from alembic.config import Config
from alembic import command

from etiket.db.data_access_objects.user import dao_user, UserType
from etiket.db.data_models.user import UserCreate
from etiket.db.get_db_session import database

from etiket.exceptions.exceptions import UserDoesNotExistException
from etiket.settings import settings


import etiket, os

# TODO check out if it should be an async engine or not!!
def _setup_db(app: FastAPI):
    app.state.db_engine = database.get_engine()
    app.state.db_session_factory = database.get_session_factory()

def _init_db(app : FastAPI):
    with app.state.db_engine.connect() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS unaccent"))
    
    with app.state.db_engine.begin() as connection:
        etiket_directory = os.path.dirname(os.path.dirname(etiket.__file__))
        alembic_cfg = Config(os.path.join(etiket_directory, 'alembic.ini'))
        alembic_cfg.attributes['connection'] = connection
        alembic_cfg.set_main_option("script_location",
                        f"{os.path.dirname(etiket.__file__)}/db/alembic")
        command.upgrade(alembic_cfg, "head")

    with app.state.db_session_factory() as session:
        user_info = {"username" : settings. ETIKET_ADMIN_USERNAME,
                "password" : settings.ETIKET_ADMIN_PASSWORD,
                "firstname" : "admin",
                "lastname" : "admin",
                "email" : settings.ETIKET_ADMIN_EMAIL,
                "user_type" : UserType.superuser}
        system_administrator = UserCreate.model_validate(user_info, context={"allow_sudo" : True})
        try:
            dao_user.read(system_administrator.username, False, session)
        except UserDoesNotExistException:
            dao_user.create(system_administrator, session)
        

def register_startup_event(app: FastAPI,):
    @app.on_event("startup")
    def _startup():
        app.middleware_stack = None
        _setup_db(app)
        _init_db(app)
    return _startup

def register_shutdown_event(app: FastAPI):
    @app.on_event("shutdown")
    def _shutdown() -> None:
        app.state.db_engine.dispose()

    return _shutdown
