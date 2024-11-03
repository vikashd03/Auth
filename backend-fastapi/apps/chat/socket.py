import asyncio
import socketio

from apps.auth.schemas import UserModel
from .schemas import ChatModel
from config import ALLOWED_ORIGINS
from .utils import ASGI_SCOPE, SIO_EVENT

sio = socketio.AsyncServer(cors_allowed_origins=ALLOWED_ORIGINS, async_mode="asgi")
app = socketio.ASGIApp(sio, socketio_path="/ws/socket.io")

USER_POOL = {}
SESSION_POOL = {}


@sio.on(SIO_EVENT.CONNECT)
async def connect(sid, environ):
    scope = environ[ASGI_SCOPE]
    user: UserModel = scope["state"].get("user")
    print(f"Client {sid} connected with user -", user.email)
    SESSION_POOL[sid] = user.id
    if user.id in USER_POOL:
        USER_POOL[user.id].append(sid)
    else:
        USER_POOL[user.id] = [sid]
    print(USER_POOL, SESSION_POOL)
    await sio.emit(event=SIO_EVENT.CONNECTED, to=sid)


@sio.on(SIO_EVENT.DISCONNECT)
async def disconnect(sid):
    print(f"Client {sid} disconnected")
    user_id = SESSION_POOL[sid]
    del SESSION_POOL[sid]
    USER_POOL[user_id].remove(sid)
    if len(USER_POOL[user_id]) == 0:
        del USER_POOL[user_id]
    print(USER_POOL, SESSION_POOL)


@sio.on("message")
async def send_message(sid, data):
    print(f"Client {sid} message -", data)
    await sio.emit(event="sent", to=sid)


async def broadcast_new_chat(chat: ChatModel):
    broadcast_tasks = []
    member_ids = [member.id for member in chat.members]
    for user_id in USER_POOL:
        if user_id in member_ids:
            for sid in USER_POOL[user_id]:
                broadcast_tasks.append(
                    sio.emit(event=SIO_EVENT.NEW_CHAT, data=chat.model_dump(), to=sid)
                )
    await asyncio.gather(*broadcast_tasks)
    print("Broadcasted event to available chat members-", SIO_EVENT.NEW_CHAT, chat.name)
