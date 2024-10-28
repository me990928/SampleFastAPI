""" This file contains the schema for the tag model """
# このスキームを使用して、タグのリクエストボディとレスポンスボディを定義します。

from pydantic import BaseModel

class TagBase(BaseModel):
    """ Tag base schema """
    name: str

class TagCreate(TagBase):
    """ Tag create schema """


class TagResponse(TagBase):
    """ Tag response schema """
    id: int
    class Config:
        """ Pydantic config """
        from_attributes = True
