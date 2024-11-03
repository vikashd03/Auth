import { Socket } from "socket.io-client";

export interface Subscriber {
  id: string;
  handler: (message: string) => void;
}

export interface Topic {
  [name: string]: Subscriber[];
}

export interface User {
  id: number;
  name: string;
  email: string;
}

export interface UserInitialState {
  access_token: string | null;
  user: User | null;
}

export interface ChatInitialState {
  socket: Socket | null;
  chats: Chat[];
}

export interface User {
  id: number;
  name: string;
  email: string;
  active: boolean;
}

export interface UsersResponse {
  data: {
    data: User[];
    total: number;
  };
  meta: any;
}

export interface Chat {
  id: number;
  type: string;
  name: string;
}

export interface ChatsResponse {
  data: {
    data: Chat[];
    total: number;
  };
  meta: any;
}
