from etiket.exceptions.exceptions import UserAlreadyExistsException,\
    UserMailAlreadyRegisteredException, UserDoesNotExistException
from etiket.db.data_models.user import UserCreate, UserRead, UserUpdate, UserReadWithScopes, UserLogin
from etiket.db.models import Users
from etiket.db.types import UserType
from passlib.context import CryptContext

from etiket.db.data_access_objects.base import dao_base

from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session, lazyload, selectinload

class dao_user(dao_base):
    @staticmethod
    def create(userCreate : UserCreate, session : Session):
        if not dao_user._unique(Users, Users.username == userCreate.username, session):
            raise UserAlreadyExistsException(userCreate.username)
        if not dao_user._unique(Users, Users.email == userCreate.email, session):
            raise UserMailAlreadyRegisteredException(userCreate.email)
        
        # hash is very slow (0.25s), this is meant to be.
        userCreate.password = _get_password_hash(userCreate.password)
        return dao_user._create(userCreate, Users, session)

    @staticmethod
    def read(username : str, read_scopes : bool, session : Session):
        user = _get_user_raw(username, session, lazy= not read_scopes)
        if read_scopes == True:
            return UserReadWithScopes.model_validate(user)
        return UserRead.model_validate(user)

    @staticmethod
    def read_all(session : Session, username_query : str = None,
                 user_type : UserType = None, offset : int = None, limit :int=None):
        return dao_user._read_all(Users, UserRead, session,
                                   string_query = {Users.username : username_query},
                                   is_equal_query ={Users.user_type : user_type},
                                   orderby = Users.username, offset=offset, limit=limit)
            
    @staticmethod
    def update(username : str, userUpdate : UserUpdate, session : Session):
        user = _get_user_raw(username, session)
        if hasattr(userUpdate, 'password') and userUpdate.password:
            userUpdate.password = _get_password_hash(userUpdate.password)
        dao_user._update(user, userUpdate, session)
        
    @staticmethod
    def delete(username : str, session : Session):
        user = _get_user_raw(username, session)
        session.delete(user)
        session.commit()

    @staticmethod
    def authenticate(username : str, password : str, session : Session):
        user = _get_user_raw(username, session)
        if (user.username == username and
                _verify_password(password, user.password)):
            return True
        return False

def _get_user_raw(username: str, session:Session, lazy=True) -> Users:
    try:
        stmt = select(Users).where(Users.username == username)
        if lazy == False:
            stmt.options(selectinload(Users.scopes))
        return session.execute(stmt).scalars().one()
    except:
        raise UserDoesNotExistException(username)
    
def _verify_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def _get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)