import { apiClient } from "./client";
import type { Vehicle, VehicleCreate } from "../types";

export const listVehicles = (skip = 0, limit = 100): Promise<Vehicle[]> =>
  apiClient
    .get<Vehicle[]>("/vehicles/", { params: { skip, limit } })
    .then((r) => r.data);

export const createVehicle = (data: VehicleCreate): Promise<Vehicle> =>
  apiClient.post<Vehicle>("/vehicles/", data).then((r) => r.data);

export const getVehicle = (id: string): Promise<Vehicle> =>
  apiClient.get<Vehicle>(`/vehicles/${id}`).then((r) => r.data);

export const getVehicleByPlate = (plate: string): Promise<Vehicle> =>
  apiClient.get<Vehicle>(`/vehicles/by-plate/${plate}`).then((r) => r.data);

export const deleteVehicle = (id: string): Promise<void> =>
  apiClient.delete(`/vehicles/${id}`).then(() => undefined);
