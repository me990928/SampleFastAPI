from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from database import Base


# 中間テーブルを定義
todo_tag_association = Table(
    "todo_tag_association",
    Base.metadata,
    Column("todo_id", Integer, ForeignKey("todos.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class Tag(Base):
    """ Tag model """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Todoとのリレーション
    # secondaryで中間テーブルを指定
    # back_populatesで関連付けられたクラスを指定
    #   ->TodoクラスのtagプロパティにはTagクラスのインスタンスが格納される
    todos = relationship("Todo", secondary=todo_tag_association, back_populates="tag")

    def __repr__(self):
        """ Tagの名前を返す """
        return f"<Tag(name={self.name})>"
