import { configureStore } from "@reduxjs/toolkit";
import packagesReducer from "./slices/packagesSlice";
import vehiclesReducer from "./slices/vehiclesSlice";
import hubsReducer from "./slices/hubsSlice";
import routesReducer from "./slices/routesSlice";

export const store = configureStore({
  reducer: {
    packages: packagesReducer,
    vehicles: vehiclesReducer,
    hubs: hubsReducer,
    routes: routesReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
