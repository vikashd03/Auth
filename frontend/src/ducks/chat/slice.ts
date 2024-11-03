import { createSlice } from "@reduxjs/toolkit";
import { ChatInitialState } from "../../types/common";
import { io } from "socket.io-client";
import { AppThunk } from "../store";

export const chatSlice = createSlice({
  name: "user",
  initialState: { socket: null, chats: [] } as ChatInitialState,
  reducers: {
    setSocket: (state, action) => {
      state.socket = action.payload;
    },
    disconnectSocket: (state) => {
      if (state.socket) {
        state.socket.disconnect();
        state.socket = null;
      }
    },
    setChats: (state, action) => {
      state.chats = action.payload;
    },
  },
});

export const { setSocket, disconnectSocket, setChats } = chatSlice.actions;

export const initializeSocket = (): AppThunk => (dispatch, getState) => {
  const accessToken = getState().user.access_token;
  const socket = io("wss://localhost:8090/", {
    path: "/ws/socket.io",
    transports: ["websocket"],
    query: {
      authorization: `Bearer ${accessToken}`,
    },
    reconnectionAttempts: 1,
    withCredentials: false,
  });
  socket.on("connected", () => {
    console.log("ws connected");
    dispatch(setSocket(socket));
  });
  socket.on("connect_error", () => {
    console.log("ws error");
    dispatch(setSocket(null));
  });
};

export default chatSlice.reducer;
