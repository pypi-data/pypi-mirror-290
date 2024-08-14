from etiket.db.get_db_session import Session, get_db_session
from etiket.web.permissions.permissions import is_any, is_scope_admin, is_admin, is_admin_type

from fastapi import APIRouter, Depends, Path, Query, status

from etiket.db.data_access_objects.user import dao_user, UserType

from etiket.db.data_models.user import UserCreate, UserReadWithScopes, UserUpdateMe, UserUpdate, UserRead, UserPasswordUpdate
from etiket.db.data_models.token import AccessToken
from etiket.exceptions.exceptions import AdminUserException, IncorrectUsernamePasswordException
from typing import List, Optional

import datetime

router = APIRouter(tags=["user"])

# TODO @alberto when searching for users -- do we need a difference between searching for 
# user with scopes loaded and without.

@router.post("/user/", status_code=status.HTTP_201_CREATED)
def create_user(*, userCreate: UserCreate,
                        accessToken: AccessToken = Depends(is_admin_type),
                        session: Session = Depends(get_db_session) ):
    dao_user.create(userCreate, session)

@router.get("/user/", response_model=UserReadWithScopes)
def get_user(*, username: str,
                        accessToken: AccessToken = Depends(is_scope_admin),
                        session: Session = Depends(get_db_session) ):
    return dao_user.read(username, read_scopes=True, session=session)

@router.get("/users/", response_model=List[UserRead])
def get_users(*, name_query : Optional[str] = None,
                        user_type: Optional[UserType]=None,
                        offset: int = 0,
                        limit: int = Query(default=800, le=1000),
                        accessToken: AccessToken = Depends(is_admin_type),
                        session: Session = Depends(get_db_session) ):
    return dao_user.read_all(username_query=name_query, user_type=user_type,
                              offset=offset, limit=limit, session=session)

@router.get("/user/me/", response_model=UserReadWithScopes)
def get_my_user_info(*, accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    return dao_user.read(accessToken.sub, read_scopes=True, session=session)

@router.patch("/user/me", status_code=status.HTTP_202_ACCEPTED)
def update_me(*, username: str,
                         userUpdate: UserUpdateMe,
                         accessToken: AccessToken = Depends(is_any),
                         session: Session = Depends(get_db_session) ):
    if accessToken.user_type == UserType.standard_user and username!=accessToken.sub:
        raise AdminUserException
    dao_user.update(username, userUpdate, session)

@router.patch("/user/update_password", status_code=status.HTTP_202_ACCEPTED)
def update_password(*, passwordUpdate: UserPasswordUpdate,
                    accessToken: AccessToken = Depends(is_any),
                    session: Session = Depends(get_db_session) ):
    if accessToken.user_type == UserType.standard_user and passwordUpdate.username!=accessToken.sub:
        raise AdminUserException
    
    auth = dao_user.authenticate(passwordUpdate.username, passwordUpdate.password, session)
    if auth is False:
        raise IncorrectUsernamePasswordException
        
    dao_user.update(passwordUpdate.username, UserUpdate(password=passwordUpdate.new_password), session)

@router.patch("/user", status_code=status.HTTP_202_ACCEPTED)
def update_user(*, username: str,
                         userUpdate: UserUpdate,
                         accessToken: AccessToken = Depends(is_admin),
                         session: Session = Depends(get_db_session) ):
    dao_user.update(username, userUpdate, session)
    
@router.delete("/user/", status_code=status.HTTP_200_OK)
def delete_user(*, username: str,
                         accessToken: AccessToken = Depends(is_admin),
                         session: Session = Depends(get_db_session) ):
    dao_user.delete(username, session)
    
@router.patch("/user/promote", status_code=status.HTTP_200_OK)
def promote_user(*, username: str,
                         user_type : UserType,
                         accessToken: AccessToken = Depends(is_admin),
                         session: Session = Depends(get_db_session) ):
    dao_user.update(username, UserUpdate(user_type=user_type), session)

@router.patch("/user/disable_on", status_code=status.HTTP_200_OK)
def disable_user_on_date(username: str,
                               disable_on : datetime.datetime,
                         accessToken: AccessToken = Depends(is_admin),
                         session: Session = Depends(get_db_session) ):
    dao_user.update(username, UserUpdate(disable_on=disable_on), session)

@router.patch("/user/disable", status_code=status.HTTP_200_OK)
def disable_user(*, username: str,
                         accessToken: AccessToken = Depends(is_admin),
                         session: Session = Depends(get_db_session) ):
    dao_user.update(username, UserUpdate(active=False), session)

@router.patch("/user/enable", status_code=status.HTTP_200_OK)
def enable_user(*, username: str,
                         accessToken: AccessToken = Depends(is_admin),
                         session: Session = Depends(get_db_session) ):
    dao_user.update(username, UserUpdate(active=True), session)