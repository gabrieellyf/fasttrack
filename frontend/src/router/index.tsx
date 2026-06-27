import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Provider } from "react-redux";
import { store } from "../store";
import { HubLayout, FeatureLayout } from "../components/Layout";
import { HubCentral } from "../features/hub/HubCentral";
import { RouteCalculator } from "../features/routes/RouteCalculator";
import { PackageList } from "../features/packages/PackageList";
import { VehicleList } from "../features/vehicles/VehicleList";
import { HubList } from "../features/hubs/HubList";

export function AppRouter() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <Routes>
          {}
          <Route element={<HubLayout />}>
            <Route path="/" element={<HubCentral />} />
          </Route>

          {}
          <Route element={<FeatureLayout />}>
            <Route path="/routing" element={<RouteCalculator />} />
            <Route path="/packages" element={<PackageList />} />
            <Route path="/vehicles" element={<VehicleList />} />
            <Route path="/hubs" element={<HubList />} />
          </Route>

          {}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </Provider>
  );
}
