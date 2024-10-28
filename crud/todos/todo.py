""" TodoのCRUD操作を行うモジュール """

import logging
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.future import select

from fastapi import Depends, HTTPException

from schema.todoSchema.tag import TagResponse
from schema.todoSchema.todo import TodoCreate, TodoResponse
from database import get_db
from model.todoModels.todo import Todo
from model.todoModels.tag import Tag, todo_tag_association


def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """ Todoを作成する """
    db_todo = Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    # db_todoからidを取得
    res = TodoResponse(id=db_todo.id, title=db_todo.title, description=db_todo.description)
    return res

def get_todo_all(db: Session = Depends(get_db)):
    """ 全てのTodoを取得する """
    todos = db.query(Todo).options(selectinload(Todo.tag)).all()
    if not todos:
        raise HTTPException(status_code=404, detail="Todoが存在しません")
    res = [TodoResponse(
        id=todo.id, title=todo.title, description=todo.description, 
        tags=[TagResponse(id=tag.id, name=tag.name) for tag in todo.tag]
        ) for todo in todos]
    return res

def get_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    """ IDでTodoを取得する """
    res = db.execute(
        select(Todo).options(joinedload(Todo.tag)).where(Todo.id == todo_id)
    ).unique().scalar_one_or_none()
    if not res:
        raise HTTPException(status_code=404, detail="Todoが存在しません")
    res = TodoResponse(
        id=res.id, title=res.title, description=res.description, 
        tags=[TagResponse(id=tag.id, name=tag.name) for tag in res.tag]
        )
    return res

def todo_in_tag(todo_id: int, tag_id: int, db: Session = Depends(get_db)):
    """ TagにTodoを追加する """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not tag or not todo:
        raise HTTPException(status_code=404, detail="TagまたはTodoが存在しません")
    todo.tag.append(tag)
    db.commit()
    db.refresh(todo)
    result = db.execute(
        select(Todo)
        .options(joinedload(Todo.tag))
        .where(Todo.id == todo_id)
    ).unique().scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail="Todoが存在しません")
    res = TodoResponse(
        id=todo.id, title=todo.title, description=todo.description, 
        tags=[TagResponse(id=tag.id, name=tag.name) for tag in todo.tag]
        )
    return res

logging.basicConfig(level=logging.INFO)

def todo_delete(todo_id: int, db: Session = Depends(get_db)):
    """ Todoを削除する """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todoが存在しません")
    # association_exists = db.query(todo_tag_association).
    # filter(todo_tag_association.c.todo_id == todo_id).all()
    association_exists = db.query(todo_tag_association).filter_by(todo_id=todo_id).all()
    if association_exists:
        db.execute(
            todo_tag_association.delete().where(todo_tag_association.c.todo_id == todo_id)
        )
    db.delete(todo)
    db.commit()
    return {"message": "Todoが削除されました"}

async def delete_tag_from_todo(todo_id: int, tag_id: int, db: Session = Depends(get_db)):
    """ 中間テーブルにTodoとTagの関連が存在するか確認 """
    association_exists = (
        db.query(todo_tag_association)
        .filter(todo_tag_association.c.todo_id == todo_id, todo_tag_association.c.tag_id == tag_id)
        .first()
    )

    if not association_exists:
        raise HTTPException(status_code=404, detail="Tag is not associated with the specified Todo")

    # 関連が存在する場合は削除
    db.execute(
        todo_tag_association.delete()
        .where(todo_tag_association.c.todo_id == todo_id)
        .where(todo_tag_association.c.tag_id == tag_id)
    )

    # 変更を保存
    db.commit()
    return {"message": f"Tag {tag_id} removed from Todo {todo_id}"}
