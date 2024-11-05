from typing import List, Optional
from sqlalchemy.orm import joinedload

from apps.auth.utils import get_profile_image_url
from internal.db import get_db

from apps.auth.models import User
from .models import Chat, chat_members
from .schemas import ChatModel
from .utils import ChatJoins, ChatType


class ChatTable:
    def create_chat(
        self, name: str, type: ChatType, members_emails: List[str]
    ) -> Optional[ChatModel]:
        with get_db() as db:
            members = db.query(User).filter(User.email.in_(members_emails)).all()
            chat = Chat(name=name, type=type, members=members)
            db.add(chat)
            db.commit()
            db.refresh(instance=chat, attribute_names=[ChatJoins.MEMBERS])
            if chat:
                return ChatModel.model_validate(chat)
            else:
                return None

    def get_chat_for_chat_id(
        self, chat_id: int, joins: List[ChatJoins] = []
    ) -> Optional[ChatModel]:
        with get_db() as db:
            join_options = []
            if len(joins) > 0:
                join_options = [joinedload(getattr(Chat, join)) for join in joins]
            chat = (
                db.query(Chat).options(*join_options).filter(Chat.id == chat_id).first()
            )
            return chat

    def get_chats_for_user_id(
        self, user_id: int, offset: int = 0, limit: int = 15
    ) -> List[ChatModel]:
        with get_db() as db:
            chats: List[ChatModel] = (
                db.query(Chat)
                .join(chat_members)
                .filter(chat_members.c.user_id == user_id)
                .offset(offset=offset)
                .limit(limit=limit)
                .all()
            )
            for chat in chats:
                if chat.type == ChatType.DIRECT:
                    member = next(
                        (member for member in chat.members if member.id != user_id),
                        None,
                    )
                    chat.name = member.name
                    img_id = member.id
                else: 
                    img_id = chat.id
                chat.img_url = get_profile_image_url(img_id, chat.type)
            return chats or []


Chats = ChatTable()
