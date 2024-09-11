import { createSlice } from '@reduxjs/toolkit';
import { InitialState } from '../../types/common';

export const userSlice = createSlice({
  name: 'user',
  initialState: { access_token: null, user: null } as InitialState,
  reducers: {
    setAccessToken: (state, action) => {
      state.access_token = action.payload
    },
    setUser: (state, action) => {
      state.user = action.payload
    }
  }
});

export const { setAccessToken, setUser } = userSlice.actions

export default userSlice.reducer;