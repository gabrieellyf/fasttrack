import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { listHubs } from "../../api/hubs";
import type { Hub } from "../../types";

export interface HubsState {
  items: Hub[];
  loading: boolean;
  error: string | null;
}

const initialState: HubsState = { items: [], loading: false, error: null };

export const fetchHubs = createAsyncThunk("hubs/list", () => listHubs());

const hubsSlice = createSlice({
  name: "hubs",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchHubs.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchHubs.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchHubs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Failed to load hubs";
      });
  },
});

export default hubsSlice.reducer;
