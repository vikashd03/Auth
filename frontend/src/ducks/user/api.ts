import { apiSlice, commonTransformResponse } from "../api/slice";
import { setUser } from "./slice";

export const userApi = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    login: builder.mutation({
      query: (data) => ({
        url: "signin/",
        method: "POST",
        body: data,
        credentials: "include",
      }),
      transformResponse: commonTransformResponse,
    }),
    register: builder.mutation({
      query: (data) => ({
        url: "signup/",
        method: "POST",
        body: data,
        credentials: "include",
      }),
      transformResponse: commonTransformResponse
    }),
    logout: builder.mutation({
      query: () => ({
        url: "logout/",
        method: "POST",
        credentials: "include",
      }),
      transformResponse: commonTransformResponse
    }),
    refresh: builder.mutation({
      query: () => ({
        url: "refresh/token/",
        method: "GET",
        credentials: "include",
      }),
      transformResponse: commonTransformResponse,
    }),
    getUsers: builder.mutation({
      query: () => ({
        url: "users/",
        method: "GET",
      }),
    }),
    getUser: builder.mutation({
      query: () => ({
        url: "user/",
        method: "GET",
      }),
      async onQueryStarted(_arg, { dispatch, queryFulfilled }) {
        try {
          const res = await queryFulfilled
          dispatch(setUser(res.data))
        } catch (err) {
          console.log('err -', err)
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