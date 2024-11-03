import { ChatsResponse } from "../../types/common";
import { apiSlice, commonTransformResponse } from "../api/slice";
import { setChats } from "./slice";

const CHAT_BASE = "/chat";

export const chatApi = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    createNewChat: builder.mutation({
      query: (data) => ({
        url: CHAT_BASE + "/new",
        method: "POST",
        body: data,
      }),
      transformResponse: commonTransformResponse,
    }),
    getChats: builder.mutation<ChatsResponse, any>({
      query: () => ({
        url: CHAT_BASE + "/list",
        method: "GET",
      }),
      transformResponse: commonTransformResponse,
      async onQueryStarted(_, { dispatch, queryFulfilled }) {
        try {
          const { data } = await queryFulfilled;
          dispatch(setChats(data?.data?.data ?? []));
        } catch (error) {
          console.error("Failed to load chats:", error);
        }
      },
    }),
  }),
});

export const { useCreateNewChatMutation, useGetChatsMutation } = chatApi;
