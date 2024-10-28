""" async_api.py """
# 非同期通信を行いうにはgreenletをインストールする必要がある
# pip install greenlet

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from model.todoModels.todo import Todo
from schema.todoSchema.tag import TagResponse
from schema.todoSchema.todo import TodoResponse
from async_database import get_db

router = APIRouter()

@router.get("/async/todos",response_model=list[TodoResponse], tags=["async"])
async def async_get_all_todos(db: AsyncSession = Depends(get_db)):
    """ 全てのTodoを取得する """
    return await get_all_todos(db)

async def get_all_todos(db: AsyncSession):
    """ 全てのTodoを取得する """
    res = await db.execute(select(Todo).options(selectinload(Todo.tag)))
    todos = res.scalars().all()
    todosres = [TodoResponse(
        id=todo.id, title=todo.title, description=todo.description,
        tags=[TagResponse(id=tag.id, name=tag.name) for tag in todo.tag]
    ) for todo in todos]
    return todosres
