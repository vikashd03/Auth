import { Action, configureStore, ThunkAction } from "@reduxjs/toolkit";
import userReducer from "./user/slice";
import chatReducer from "./chat/slice";
import { apiSlice } from "./api/slice";

export const store = configureStore({
  reducer: {
    user: userReducer,
    chat: chatReducer,
    [apiSlice.reducerPath]: apiSlice.reducer,
  },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware({serializableCheck: false}).concat(apiSlice.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;