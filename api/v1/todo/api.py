""" This module contains the API routes for the todo app """

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from crud.todos.tag import create_tag, get_tag_all, get_tag_by_id, delete_tag
from crud.todos.todo import (
    create_todo, delete_tag_from_todo, get_todo_all,
    get_todo_by_id, todo_in_tag, todo_delete
)
from schema.todoSchema.tag import TagCreate, TagResponse
from schema.todoSchema.todo import TodoResponse, TodoCreate

router = APIRouter()

@router.post("/todos", response_model=TodoResponse, tags=["todos"])
def insert_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """ Create a new todo in the database """
    return create_todo(db=db, todo=todo)

@router.post("/tags", response_model=TagResponse, tags=["todos"])
def insert_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """ Create a new tag in the database """
    return create_tag(db=db, tag=tag)

@router.get("/todos", response_model=List[TodoResponse], tags=["todos"])
def get_todos(db: Session = Depends(get_db)):
    """ Get all todos from the database """
    return get_todo_all(db)

@router.get("/tags", response_model=List[TagResponse], tags=["todos"])
def get_tags(db: Session = Depends(get_db)):
    """ Get all tags from the database """
    return get_tag_all(db)

@router.get("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
def get_todos_by_id(todo_id: int, db: Session = Depends(get_db)):
    """ Get a todo by its id """
    return get_todo_by_id(todo_id, db)

@router.get("/tags/{tag_id}", response_model=TagResponse, tags=["todos"])
def get_tags_by_id(tag_id: int, db: Session = Depends(get_db)):
    """ Get a tag by its id """
    return get_tag_by_id(tag_id, db)

@router.post("/todos/{todo_id}/tags/{tag_id}", response_model=TodoResponse, tags=["todos"])
def add_tag_to_todo(todo_id: int, tag_id: int, db: Session = Depends(get_db)):
    """ Add a tag to a todo """
    return todo_in_tag(todo_id, tag_id, db)

@router.delete("/todos/{todo_id}", response_model=dict, tags=["todos"])
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """ Delete a todo by its id """
    return todo_delete(todo_id, db)

@router.delete("/todos/{todo_id}/tags/{tag_id}", tags=["todos"])
def delete_tag_from_todo_association(todo_id: int, tag_id: int, db: Session = Depends(get_db)):
    """ Delete a tag from a todo """
    return delete_tag_from_todo(todo_id, tag_id, db)

@router.delete("/tags/{tag_id}", response_model=dict, tags=["todos"])
async def delete_tags(tag_id: int, db: Session = Depends(get_db)):
    """ Delete a tag by its id """
    return delete_tag(tag_id, db)
