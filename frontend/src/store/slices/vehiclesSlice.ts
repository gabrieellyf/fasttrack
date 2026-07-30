import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { listVehicles, createVehicle } from "../../api/vehicles";
import type { Vehicle, VehicleCreate } from "../../types";

export interface VehiclesState {
  items: Vehicle[];
  loading: boolean;
  error: string | null;
}

const initialState: VehiclesState = { items: [], loading: false, error: null };

export const fetchVehicles = createAsyncThunk("vehicles/list", () =>
  listVehicles(),
);

export const addVehicle = createAsyncThunk(
  "vehicles/create",
  (data: VehicleCreate) => createVehicle(data),
);

const vehiclesSlice = createSlice({
  name: "vehicles",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchVehicles.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchVehicles.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchVehicles.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Failed to load vehicles";
      })
      .addCase(addVehicle.fulfilled, (state, action) => {
        state.items.push(action.payload);
      });
  },
});

export default vehiclesSlice.reducer;
