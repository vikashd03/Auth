from fastapi import FastAPI, HTTPException, Response, status

from .socket import broadcast_new_chat
from .utils import ChatJoins, check_chat_access
from internal.utils import AppRequest, register_exception_handlers

from .schemas import (
    ChatMessagesResponse,
    ChatMembersResponse,
    CreateChatFormData,
    CreateChatResponse,
)
from .crud import Chats


app = FastAPI()

register_exception_handlers(app)


@app.get("/messages/{chat_id}", response_model=ChatMessagesResponse)
def get_messages(request: AppRequest, response: Response, chat_id: int):
    chat = Chats.get_chat_for_chat_id(
        chat_id=chat_id, joins=[ChatJoins.MEMBERS, ChatJoins.MESSAGES]
    )
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Chat Not Found"
        )
    check_chat_access(chat=chat, user=request.state.user)
    response.status_code = status.HTTP_200_OK
    return {"data": chat.messages, "total": len(chat.messages)}


@app.get("/members/{chat_id}", response_model=ChatMembersResponse)
def get_members(request: AppRequest, response: Response, chat_id: int):
    chat = Chats.get_chat_for_chat_id(chat_id=chat_id, joins=[ChatJoins.MEMBERS])
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Chat Not Found"
        )
    check_chat_access(chat=chat, user=request.state.user)
    response.status_code = status.HTTP_200_OK
    return {"data": chat.members, "total": len(chat.members)}


@app.post("/new", response_model=CreateChatResponse)
async def new_chat(
    request: AppRequest, response: Response, form_data: CreateChatFormData
):
    user = request.state.user
    chat_type = form_data.type
    members_emails = [*form_data.members, user.email]
    chat_name = form_data.name
    chat = Chats.create_chat(
        name=chat_name,
        type=chat_type,
        members_emails=members_emails,
    )
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in creating new Chat",
        )
    await broadcast_new_chat(chat=chat)
    response.status_code = status.HTTP_200_OK
    return {"msg": "New Chat Created", "chat": chat}


@app.get("/list")
async def my_chats(request: AppRequest, response: Response):
    user = request.state.user
    chats = Chats.get_chats_for_user_id(user_id=user.id)
    response.status_code = status.HTTP_200_OK
    return {
        "data": chats,
        "total": len(chats),
    }
