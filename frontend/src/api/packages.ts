import { apiClient } from "./client";
import type { Package, PackageCreate, PackageUpdate } from "../types";

export const listPackages = (skip = 0, limit = 100): Promise<Package[]> =>
  apiClient
    .get<Package[]>("/packages/", { params: { skip, limit } })
    .then((r) => r.data);

export const createPackage = (data: PackageCreate): Promise<Package> =>
  apiClient.post<Package>("/packages/", data).then((r) => r.data);

export const getPackage = (id: string): Promise<Package> =>
  apiClient.get<Package>(`/packages/${id}`).then((r) => r.data);

export const updatePackage = (
  id: string,
  data: PackageUpdate,
): Promise<Package> =>
  apiClient.patch<Package>(`/packages/${id}`, data).then((r) => r.data);

export const deletePackage = (id: string): Promise<void> =>
  apiClient.delete(`/packages/${id}`).then(() => undefined);
