""" This module defines the API routes for the FastAPI application. """

from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from crud.user import create_user, create_user_data
from database import get_db
from model.user import User
from schema.user import (
    UserAndDataResponse, UserCreate, UserDataCreate, UserDataResponse, UserResponse
)

# ルーターを作成
router = APIRouter()

# ルートエンドポイントを作成
@router.get("/", tags=["root"])
def read_root():
    """ Default route to check if the API is running 
        Returns:
        dict: A simple message to show the API is running
    """
    return {"message": "Welcome to your API!"}


@router.post("/users/", response_model=UserResponse)
def api_create_user(user: UserCreate, db: Session = Depends(get_db)):
    """ ユーザーをデータベースに作成する """
    return create_user(db=db, user=user)

@router.post("/user_data/", response_model=UserDataResponse)
def api_create_user_data(user_data: UserDataCreate, db: Session = Depends(get_db)):
    """ ユーザーデータをデータベースに作成する """
    return create_user_data(db=db, user_data=user_data)

@router.get("/api/users/{user_id}", response_model=UserAndDataResponse)
def get_user_with_data(user_id: int, db: Session = Depends(get_db)):
    """ ユーザーとユーザーデータを取得する """
    result = db.execute(
        select(User)
        .options(joinedload(User.data))
        .where(User.id == user_id)
    ).unique()
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
