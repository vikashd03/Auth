from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text, Enum as SqlEnum
from sqlalchemy.orm import relationship


from .utils import ChatRole, ChatType
from internal.db import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    content = Column(Text)
    sender_id = Column(Integer, ForeignKey("users.id"))

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User")


chat_members = Table(
    "chat_members",
    Base.metadata,
    Column("chat_id", Integer, ForeignKey("chats.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role", SqlEnum(ChatRole), default=ChatRole.MEMBER),
)


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    type = Column(SqlEnum(ChatType), default=ChatType.DIRECT)
    name = Column(String(length=50), nullable=True)

    messages = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )
    members = relationship("User", secondary=chat_members, back_populates="chats")
