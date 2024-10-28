""" Todoのスキーマモデル """
# このスキームを使用して、Todoのリクエストボディとレスポンスボディを定義します。

from typing import List, Optional
from pydantic import BaseModel

from schema.todoSchema.tag import TagResponse


class TodoBase(BaseModel):
    """ Todoのベースモデル """
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    """ Todoの作成時のリクエストボディ """

class TodoResponse(TodoBase):
    """ Todoのレスポンスボディ """
    id: int
    tags: List[TagResponse] = []

    class Config:
        """ Pydanticの設定 """
        from_attributes = True

class TagWithTodosResponse(BaseModel):
    """ タグとTodoのレスポンスボディ """
    todos: List[TodoResponse] = []

    class Config:
        """ Pydanticの設定 """
        from_attributes = True
