import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { RootState } from "../store";
import {
  MutationActionCreatorResult,
  MutationDefinition,
  QueryArgFrom,
} from "@reduxjs/toolkit/query";
import { pubsub } from "../../utils/PubSub";
import { pubsubTopic } from "../../utils/constants";
import { BASE_URI, UNPROTECTED_ENPOINTS } from "../../utils/config";

const API_REQUEST_TIMEOUT = 90000;
export const BASE_URL = BASE_URI + "api/";
export const commonTransformResponse = (data: any, meta: any) => ({
  data,
  meta,
});

export const apiSlice = createApi({
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_URL,
    timeout: API_REQUEST_TIMEOUT,
    prepareHeaders: (headers, { getState, endpoint }) => {
      console.log("endpoint -", endpoint);
      const accessToken = (getState() as RootState).user.access_token;
      if (accessToken) {
        headers.set("Authorization", `Bearer ${accessToken}`);
      }
      return headers;
    },
    responseHandler: (response: Response) => {
      let url = response.url.replace(BASE_URL, "");
      url = url.endsWith("/") ? url : url + "/";
      if (!UNPROTECTED_ENPOINTS.includes(url) && response.status === 401) {
        console.log(url, ": Unauthorized, logging out...");
        pubsub.publish(pubsubTopic.AUTH_LOGOUT, "logout");
      }
      return response.json();
    },
  }),
  reducerPath: "api",
  tagTypes: ["User", "Chat"],
  endpoints: () => ({}),
});

export type MutationTrigger<D extends MutationDefinition<any, any, any, any>> =
  (arg: QueryArgFrom<D>) => MutationActionCreatorResult<D>;
