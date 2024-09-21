import { Route, Routes } from "react-router-dom";
import { pubsub } from "./utils/PubSub";
import { pubsubTopic } from "./utils/constants";
import useNavigateWithState from "./hooks/useNavigateWithState";
import Home from "./pages/home";
import Profile from "./pages/profile";
import Chat from "./pages/chat";
import "./index.scss";

const Layout = () => {
  const navigate = useNavigateWithState();

  return (
    <div className="main-layout">
      <div>inside Layout</div>
      <Routes>
        <Route path="home" Component={Home} />
        <Route path="profile" Component={Profile} />
        <Route path="chat" Component={Chat} />
        <Route path="*" element={<div>Page Not Found</div>} />
      </Routes>
      <div className="layout-btns">
        <button
          onClick={() => {
            navigate("/home");
          }}
        >
          Home
        </button>
        <button
          onClick={() => {
            navigate("/chat");
          }}
        >
          Chat
        </button>
        <button
          onClick={() => {
            navigate("/profile");
          }}
        >
          Profile
        </button>
        <button
          onClick={() => {
            pubsub.publish(pubsubTopic.AUTH_LOGOUT, "logout");
          }}
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default Layout;
