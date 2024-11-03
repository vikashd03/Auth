import { IoSearchSharp } from "react-icons/io5";
import { CgProfile } from "react-icons/cg";
import { HiUserGroup } from "react-icons/hi";
import "./index.scss";
import { useState } from "react";
import NewChatModal from "../NewGrpChatModal";
import { RootState } from "../../ducks/store";
import { useSelector } from "react-redux";

const ChatList = () => {
  const [newChatModalOpen, setNewChatModalOpen] = useState(false);
  const chat = useSelector((state: RootState) => state.chat);
  const { chats } = chat;

  const handleAddNewChat = () => {
    setNewChatModalOpen(true);
  };

  return (
    <div className="chat-list-wrapper">
      {newChatModalOpen && (
        <NewChatModal
          isOpen={newChatModalOpen}
          onClose={() => setNewChatModalOpen(false)}
        />
      )}
      <div className="class-list-title-add">
        <div className="chat-list-title">My Chats</div>
        <HiUserGroup className="add-new-chat-btn" onClick={handleAddNewChat} />
      </div>
      <div className="chat-list-search">
        <IoSearchSharp className="chat-list-search-icon" />
        <input
          className="chat-list-search-input"
          placeholder="Search Contact"
        ></input>
      </div>
      <div className="chat-list">
        {chats.map((chat, index) => (
          <div className="chat-list-item" key={index}>
            <div className="chat-item-left">
              <img src={""} className="chat-item-icon" />
              <CgProfile className="chat-item-icon" />
              <div className="user-name">
                {chat.name}
              </div>
            </div>
            {/* <div className="chat-item-right">
              <div>{chat.lastMsgStatus}</div>
              <div className="last-msg">{chat.lastMsg}</div>
            </div> */}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatList;
