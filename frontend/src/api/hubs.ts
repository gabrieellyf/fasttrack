import { apiClient } from "./client";
import type { Hub, HubCreate } from "../types";

export const listHubs = (params?: { is_central?: boolean }): Promise<Hub[]> =>
  apiClient.get<Hub[]>("/hubs/", { params }).then((r) => r.data);

export const createHub = (data: HubCreate): Promise<Hub> =>
  apiClient.post<Hub>("/hubs/", data).then((r) => r.data);

export const getHub = (id: string): Promise<Hub> =>
  apiClient.get<Hub>(`/hubs/${id}`).then((r) => r.data);

export const deleteHub = (id: string): Promise<void> =>
  apiClient.delete(`/hubs/${id}`).then(() => undefined);
