""" TagのCRUD操作を行うための関数を定義するモジュール """

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from schema.todoSchema.tag import TagCreate, TagResponse
from database import get_db
from model.todoModels.tag import Tag

def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """ Todoを作成する """
    db_tag = Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    res = TagResponse(id=db_tag.id, name=db_tag.name)
    return res

def get_tag_all(db: Session = Depends(get_db)):
    """ 全てのTagを取得する """
    tags = db.query(Tag).all()
    if tags is None:
        raise HTTPException(status_code=404, detail="Tagが存在しません")
    res = [TagResponse(id=tag.id, name=tag.name) for tag in tags]
    return res

def get_tag_by_id(tag_id: int, db: Session = Depends(get_db)):
    """ IDでTagを取得する """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tagが存在しません")
    res = TagResponse(id=tag.id, name=tag.name)
    return res

def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """ IDでTagを削除する """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tagが存在しません")
    db.delete(tag)
    db.commit()
    return {"message": "Tagが削除されました"}
