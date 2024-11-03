import { createSlice } from '@reduxjs/toolkit';
import { UserInitialState } from '../../types/common';

export const userSlice = createSlice({
  name: 'user',
  initialState: { access_token: null, user: null } as UserInitialState,
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