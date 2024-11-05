import { IoSearchSharp } from "react-icons/io5";
import { CgProfile } from "react-icons/cg";
import { HiUserGroup } from "react-icons/hi";
import "./index.scss";
import { useEffect, useMemo, useState } from "react";
import NewChatModal from "../NewGrpChatModal";
import { RootState } from "../../ducks/store";
import { useSelector } from "react-redux";
import { BASE_URL } from "../../ducks/api/slice";
import { useGetUsersMutation } from "../../ducks/user/api";
import { CHAT_TYPE } from "../../types/common";

const ChatList = () => {
  const [newChatModalOpen, setNewChatModalOpen] = useState(false);
  const [chatListSearch, setChatListSearch] = useState("");
  const [getUsers, { data: usersData, isLoading: usersIsLoading }] =
    useGetUsersMutation();
  const chat = useSelector((state: RootState) => state.chat);
  const { chats } = chat;
  const usersList = usersData?.data?.data ?? [];

  useEffect(() => {
    getUsers(undefined);
  }, []);

  const filteredChatList = useMemo(() => {
    const directChatUserIds = chats
      .filter((chat) => chat.type === CHAT_TYPE.DIRECT)
      .map((chat) => chat.sender?.id);
    const usersNotInChats = usersList.filter(
      (user) => !directChatUserIds.includes(user.id)
    );
    return (
      chatListSearch !== "" ? [...chats, ...usersNotInChats] : chats
    ).filter((chat) =>
      chat.name.toUpperCase().includes(chatListSearch.toUpperCase())
    );
  }, [chats, chatListSearch, usersList]);

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
          value={chatListSearch}
          onChange={(e) => setChatListSearch(e.target.value)}
        />
      </div>
      <div className="chat-list">
        {filteredChatList.map((chat, index) => (
          <div className="chat-list-item" key={index}>
            <div className="chat-item-left">
              {chat.img_url ? (
                <img
                  src={`${BASE_URL}${chat.img_url}`}
                  className="chat-item-profile-img"
                />
              ) : (
                <CgProfile className="chat-item-profile-icon" />
              )}
              <div className="user-name">{chat.name}</div>
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
