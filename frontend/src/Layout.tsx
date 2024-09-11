import { Route, Routes } from "react-router-dom";
import Home from "./pages/home";
import { pubsub } from "./utils/PubSub";
import useNavigateWithState from "./hooks/useNavigateWithState";
import Profile from "./pages/profile";
import "./index.scss";
import { pubsubTopic } from "./utils/constants";

const Layout = () => {
  const navigate = useNavigateWithState();

  return (
    <div className="main-layout">
      <div>inside Layout</div>
      <Routes>
        <Route path="home" Component={Home} />
        <Route path="profile" Component={Profile} />
        <Route path="*" element={<div>Page Not Found</div>} />
      </Routes>
      <div className="layout-btns">
        <button
          onClick={() => {
            pubsub.publish(pubsubTopic.AUTH_LOGOUT, "logout");
          }}
        >
          Logout
        </button>
        <button
          onClick={() => {
            navigate("/login");
          }}
        >
          Login
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
            navigate("/home");
          }}
        >
          Home
        </button>
      </div>
    </div>
  );
};

export default Layout;
