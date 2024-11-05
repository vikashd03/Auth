from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from apps.auth.schemas import UserModel, UserResponse
from .utils import ChatType


class MessageModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chat_id: int
    content: str
    sender_id: int


class ChatModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: ChatType
    name: Optional[str] = None
    messages: List[MessageModel]
    members: List[UserModel]
    img_url: Optional[str] = None


class ChatResponse(BaseModel):
    id: int
    type: ChatType
    name: Optional[str] = None


class CreateChatFormData(BaseModel):
    name: Optional[str] = None
    type: ChatType
    members: List[str]


class CreateChatResponse(BaseModel):
    msg: str
    chat: ChatResponse


class ChatMessagesResponse(BaseModel):
    data: List[MessageModel]
    total: int


class ChatMembersResponse(BaseModel):
    data: List[UserResponse]
    total: int
