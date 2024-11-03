import { UsersResponse } from "../../types/common";
import { apiSlice, commonTransformResponse } from "../api/slice";
import { setUser } from "./slice";

const AUTH_BASE = "/auth";

export const userApi = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    login: builder.mutation({
      query: (data) => ({
        url: AUTH_BASE + "/signin",
        method: "POST",
        body: data,
        credentials: "include",
      }),
      transformResponse: commonTransformResponse,
    }),
    register: builder.mutation({
      query: (data) => ({
        url: AUTH_BASE + "/signup",
        method: "POST",
        body: data,
        credentials: "include",
      }),
      transformResponse: commonTransformResponse,
    }),
    logout: builder.mutation({
      query: () => ({
        url: AUTH_BASE + "/logout",
        method: "POST",
        credentials: "include",
      }),
      transformResponse: commonTransformResponse,
    }),
    refresh: builder.mutation({
      query: () => ({
        url: AUTH_BASE + "/refresh/token",
        method: "GET",
        credentials: "include",
      }),
      transformResponse: commonTransformResponse,
    }),
    getUsers: builder.mutation<UsersResponse, any>({
      query: () => ({
        url: AUTH_BASE + "/users",
        method: "GET",
      }),
      transformResponse: commonTransformResponse,
    }),
    getUser: builder.mutation({
      query: () => ({
        url: AUTH_BASE + "/user",
        method: "GET",
      }),
      async onQueryStarted(_arg, { dispatch, queryFulfilled }) {
        try {
          const res = await queryFulfilled;
          dispatch(setUser(res.data));
        } catch (err) {
          console.log("err -", err);
        }
      },
    }),
  }),
});

export const {
  useLoginMutation,
  useLogoutMutation,
  useRegisterMutation,
  useRefreshMutation,
  useGetUsersMutation,
  useGetUserMutation,
} = userApi;
