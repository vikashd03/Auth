import { useEffect } from "react";
import "./index.scss";
import { useSelector } from "react-redux";
import { RootState } from "../../ducks/store";
import ChatList from "../../components/ChatList";
import ChatBox from "../../components/ChatBox";
import { useGetChatsMutation } from "../../ducks/chat/api";

const Chat = () => {
  const chat = useSelector((state: RootState) => state.chat);
  const { socket } = chat;
  const [getChats, { isLoading: chatIsLoading }] = useGetChatsMutation();

  useEffect(() => {
    getChats(undefined);
  }, []);

  useEffect(() => {
    if (socket) {
      socket.on("message", (data) => {
        console.log("message -", data);
      });
      socket.on("new_chat", (data) => {
        console.log("new chat -", data);
      });
    }
  }, [socket]);

  return (
    <div className="chat-page-wrapper">
      <div className="chat-page-title">Chat here</div>
      <div className="chat-content-wrapper">
        <ChatList />
        <ChatBox />
      </div>
    </div>
  );
};

export default Chat;
