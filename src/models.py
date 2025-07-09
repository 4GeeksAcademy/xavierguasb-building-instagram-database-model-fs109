from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    followers = relationship("Follower", foreign_keys=lambda: [Follower.user_id], back_populates="user")
    following = relationship("Follower", foreign_keys=lambda: [Follower.follower_id], back_populates="follower_user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    like: Mapped[int] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    parent: Mapped["User"] = relationship(back_populates="posts")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "name": self.name,
            "like": self.like,
            "url": self.url
        }
    
class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user = relationship("User", foreign_keys=[user_id], back_populates="followers")
    follower_user = relationship("User", foreign_keys=[follower_id], back_populates="following")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "Follower_id": self.Follower_id
        }    