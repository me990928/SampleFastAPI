""" ユーザーに関するCRUD操作を定義します """

from sqlalchemy.orm import Session
from model.user import User, UserData
from schema.user import UserCreate, UserDataCreate

def create_user(db: Session, user: UserCreate) -> User:
    """ 新しいユーザーをデータベースに作成します """
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_data(db: Session, user_data: UserDataCreate) -> UserData:
    """ 新しいユーザーデータをデータベースに作成します """
    db_user_data = UserData(user_id=user_data.user_id, data=user_data.data)
    db.add(db_user_data)
    db.commit()
    db.refresh(db_user_data)
    return db_user_data
