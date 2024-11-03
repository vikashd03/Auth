from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


from internal.db import Base
from apps.chat.models import chat_members


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))
    email = Column(String(length=320), unique=True, index=True)
    password = Column(String(length=500))
    active = Column(Boolean, default=True)

    chats = relationship("Chat", secondary=chat_members, back_populates="members")
