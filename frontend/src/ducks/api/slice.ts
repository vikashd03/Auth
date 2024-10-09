import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
// import axios, { AxiosResponse } from "axios";
import { RootState } from "../store";
import { MutationActionCreatorResult, MutationDefinition, QueryArgFrom } from "@reduxjs/toolkit/query";
import { pubsub } from "../../utils/PubSub";
import { pubsubTopic } from "../../utils/constants";
import { BASE_URI, UNPROTECTED_ENPOINTS } from "../../utils/config";

const API_REQUEST_TIMEOUT = 90000;
export const BASE_URL = BASE_URI + "api/";
export const commonTransformResponse = (data: any, meta: any) => ({ data, meta });

// const axiosInstance = axios.create({
//   baseURL: BASE_URL,
//   timeout: API_REQUEST_TIMEOUT,
//   headers: {
//     "Content-Type": "application/json",
//   },
// });

// axiosInstance.interceptors.request.use(
//   (config) => {
//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );

// axiosInstance.interceptors.response.use(
//   (response) => {
//     return response;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );

// const axiosBaseQuery =
//   ({ baseUrl } = { baseUrl: "" }) =>
//     async ({ url, method, body, params, headers }: any) => {
//       console.log("props -", url, method, body, params, headers);
//       try {
//         const result: AxiosResponse | any = await axiosInstance({
//           url: baseUrl + url,
//           method,
//           data: body,
//           params,
//           headers,
//         });
//         const { data: resData, ...meta } = result;
//         return { data: resData, meta };
//       } catch (AxiosError) {
//         // console.log('error -', AxiosError)
//         return { error: AxiosError };
//       }
//     };

export const apiSlice = createApi({
  // baseQuery: axiosBaseQuery({
  //   baseUrl: BASE_URL,
  // }),
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_URL,
    timeout: API_REQUEST_TIMEOUT,
    prepareHeaders: (headers, { getState, endpoint }) => {
      console.log('endpoint -', endpoint)
      const accessToken = (getState() as RootState).user.access_token
      if (accessToken) {
        headers.set("Authorization", `Bearer ${accessToken}`)
      }
      return headers
    },
    responseHandler: (response: Response) => {
      const endpoint = response.url.replace(BASE_URL, '')
      if (!UNPROTECTED_ENPOINTS.includes(endpoint) && response.status === 401) {
        pubsub.publish(pubsubTopic.AUTH_LOGOUT, "logout");
      }
      return response.json()
    }
  }),
  reducerPath: "api",
  tagTypes: ["User"],
  endpoints: () => ({}),
});


export type MutationTrigger<D extends MutationDefinition<any, any, any, any>> = (arg: QueryArgFrom<D>) => MutationActionCreatorResult<D>;
