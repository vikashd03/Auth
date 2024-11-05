from enum import Enum
from fastapi import HTTPException, status
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.auth.schemas import UserModel
    from apps.chat.schemas import ChatModel

ASGI_SCOPE = "asgi.scope"


class SIO_EVENT(str, Enum):
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    CONNECTED = "connected"
    NEW_CHAT = "new_chat"


class ChatType(str, Enum):
    DIRECT = "direct"
    GROUP = "group"


class ChatRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    CREATER = "creator"


class ChatJoins(str, Enum):
    MEMBERS = "members"
    MESSAGES = "messages"


def check_chat_access(chat: "ChatModel", user: "UserModel"):
    if len(chat.members) > 0 and user.email not in [
        member.email for member in chat.members
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not part of this Chat"
        )
