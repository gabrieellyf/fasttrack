import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { listPackages, createPackage, deletePackage } from "../../api/packages";
import type { Package, PackageCreate } from "../../types";

export interface PackagesState {
  items: Package[];
  loading: boolean;
  error: string | null;
}

const initialState: PackagesState = { items: [], loading: false, error: null };

export const fetchPackages = createAsyncThunk("packages/list", () =>
  listPackages(),
);

export const addPackage = createAsyncThunk(
  "packages/create",
  (data: PackageCreate) => createPackage(data),
);

export const removePackage = createAsyncThunk("packages/delete", (id: string) =>
  deletePackage(id).then(() => id),
);

const packagesSlice = createSlice({
  name: "packages",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchPackages.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPackages.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchPackages.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Failed to load packages";
      })
      .addCase(addPackage.fulfilled, (state, action) => {
        state.items.push(action.payload);
      })
      .addCase(removePackage.fulfilled, (state, action) => {
        state.items = state.items.filter((p) => p.id !== action.payload);
      });
  },
});

export default packagesSlice.reducer;
