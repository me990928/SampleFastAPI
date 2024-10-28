""" Todo model """
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from model.todoModels.tag import todo_tag_association

class Todo(Base):
    """ Todo model """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    # Tagとのリレーション
    # secondaryで中間テーブルを指定
    # back_populatesで関連付けられたクラスを指定
    #   ->TagクラスのtodosプロパティにはTodoクラスのインスタンスが格納される
    tag = relationship("Tag",secondary=todo_tag_association, back_populates="todos")

    def __repr__(self):
        """ Todoのタイトルを返す """
        return f"<Todo(title={self.title})>"
