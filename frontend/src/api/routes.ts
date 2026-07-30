import { apiClient } from "./client";
import type { RouteRequest, RouteResponse } from "../types";

export const calculateRoutes = (
  request: RouteRequest,
): Promise<RouteResponse> =>
  apiClient.post<RouteResponse>("/routes/", request).then((r) => r.data);
