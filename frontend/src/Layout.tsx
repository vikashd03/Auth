import { Route, Routes } from "react-router-dom";
import Home from "./pages/home";
import Chat from "./pages/chat";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { disconnectSocket, initializeSocket } from "./ducks/chat/slice";
import { AppDispatch } from "./ducks/store";
import Nav from "./components/Nav";
import "./index.scss";

const Layout = () => {
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(initializeSocket());

    return () => {
      console.log('ws disconnected')
      dispatch(disconnectSocket());
    };
  }, []);

  return (
    <div className="main-layout">
      <Nav />
      <div className="page-layout">
        <Routes>
          <Route path="home" Component={Home} />
          <Route path="chat" Component={Chat} />
          <Route path="*" element={<div>Page Not Found</div>} />
        </Routes>
      </div>
    </div>
  );
};

export default Layout;
