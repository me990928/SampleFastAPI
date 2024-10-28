""" User model """

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
from database import Base

class User(Base):
    """ User model """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    data = relationship("UserData", back_populates="user")

    def __repr__(self):
        """ ユーザーの名前を返す """
        return f"<User(name={self.name})>"

# 普通なら別ファイルに書く
class UserData(Base):
    """ User data model """
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    data = Column(String)

    user = relationship("User", back_populates="data")

    def __repr__(self):
        """ ユーザーデータを返す """
        return f"<UserData(data={self.data})>"
