import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";
import { calculateRoutes } from "../../api/routes";
import type { ApiError, RouteRequest, RouteResponse } from "../../types";

export interface RoutesState {
  result: RouteResponse | null;
  loading: boolean;
  error: string | null;
  errorCode: string | null;
  errorDetails: Record<string, number> | null;
}

const initialState: RoutesState = {
  result: null,
  loading: false,
  error: null,
  errorCode: null,
  errorDetails: null,
};

export const fetchRoutes = createAsyncThunk(
  "routes/calculate",
  async (request: RouteRequest, { rejectWithValue }) => {
    try {
      return await calculateRoutes(request);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.data) {
        return rejectWithValue(err.response.data as ApiError);
      }
      throw err;
    }
  },
);

const routesSlice = createSlice({
  name: "routes",
  initialState,
  reducers: {
    clearRoutes: (state) => {
      state.result = null;
      state.error = null;
      state.errorCode = null;
      state.errorDetails = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchRoutes.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.errorCode = null;
        state.errorDetails = null;
      })
      .addCase(fetchRoutes.fulfilled, (state, action) => {
        state.loading = false;
        state.result = action.payload;
      })
      .addCase(fetchRoutes.rejected, (state, action) => {
        state.loading = false;
        const payload = action.payload as ApiError | undefined;
        state.error =
          payload?.message ??
          action.error.message ??
          "Failed to calculate routes";
        state.errorCode = payload?.error_code ?? null;
        state.errorDetails =
          (payload?.details as Record<string, number>) ?? null;
      });
  },
});

export const { clearRoutes } = routesSlice.actions;
export default routesSlice.reducer;
