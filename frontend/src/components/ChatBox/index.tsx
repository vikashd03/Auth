import { IoSearchSharp } from "react-icons/io5";
import "./index.scss";
import { CgProfile } from "react-icons/cg";
import { IoSend } from "react-icons/io5";
import { useState } from "react";

const ChatBox = () => {
  const [msgSearchVisible, setMsgSearchVisible] = useState(false);
  const messages = [
    {
      sender: "left",
      content: "hi Bro",
    },
    {
      sender: "right",
      content: "hi Bro",
    },
    {
      sender: "left",
      content: "how r u?",
    },
    {
      sender: "left",
      content: "how r u?",
    },
    {
      sender: "left",
      content: "how r u?",
    },
    {
      sender: "left",
      content: "how r u?",
    },
  ];
  return (
    <div className="chat-box-wrapper">
      <div className="profile-section-wrapper">
        <div className="profile-content">
          <CgProfile className="profile-icon" />
          <div className="profile-name">Vikash D</div>
        </div>
        <div className="messages-search">
          {msgSearchVisible && (
            <input
              className="messages-search-input"
              placeholder="search here"
            />
          )}
          <IoSearchSharp
            className="messages-search-icon"
            onClick={() => setMsgSearchVisible(!msgSearchVisible)}
          />
        </div>
      </div>
      <div className="messages-wrapper">
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{ marginLeft: msg.sender === "left" ? 0 : "auto" }}
          >
            {msg.content}
          </div>
        ))}
      </div>
      <div className="new-message-wrapper">
        <input placeholder="Enter New Message" className="new-message-input" />
        <button className="new-message-btn">
          <IoSend className="new-message-btn-icon" />
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
