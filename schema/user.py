""" ユーザーのスキーマモデル """
# このスキーマを使用してリクエストボディやレスポンスボディを定義する

from typing import List
from pydantic import BaseModel

class UserCreate(BaseModel):
    """ ユーザー作成時のリクエストボディ """
    name: str
    class Config:
        """ Pydanticの設定 """
        from_attributes = True

class UserDataCreate(BaseModel):
    """ ユーザーデータ作成時のリクエストボディ """
    user_id: int
    data: str
    class Config:
        """ Pydanticの設定 """
        from_attributes = True

class UserResponse(BaseModel):
    """ ユーザー情報のレスポンスボディ """
    id: int
    name: str

    class Config:
        # モデルの属性から値を取得する
        from_attributes = True

class UserDataResponse(BaseModel):
    """ ユーザーデータ情報のレスポンスボディ """
    id: int
    data: str

    class Config:
        # 同上
        from_attributes = True

class UserAndDataResponse(UserResponse):
    """ ユーザー情報とユーザーデータ情報のレスポンスボディ """
    data: List[UserDataResponse]

    class Config:
        # 同上
        from_attributes = True 
