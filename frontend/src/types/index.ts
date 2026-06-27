export interface Package {
  id: string;
  recipient_name: string;
  x: number;
  y: number;
  weight: number;
  access_cost: number;
  deleted: boolean;
  created_at: string;
}

export interface PackageCreate {
  recipient_name: string;
  x: number;
  y: number;
  weight: number;
  access_cost?: number;
}

export interface PackageUpdate {
  recipient_name?: string;
  x?: number;
  y?: number;
  weight?: number;
  access_cost?: number;
}

export interface Vehicle {
  id: string;
  plate: string;
  max_weight: number;
  deleted: boolean;
  created_at: string;
}

export interface VehicleCreate {
  plate: string;
  max_weight: number;
}

export interface Hub {
  id: string;
  name: string;
  x: number;
  y: number;
  is_central: boolean;
  deleted: boolean;
  created_at: string;
}

export interface HubCreate {
  name: string;
  x: number;
  y: number;
  is_central?: boolean;
}

export interface RouteStop {
  id: string;
  label: string;
  x: number;
  y: number;
}

export interface RouteOption {
  type: "express" | "economic" | "strategic";
  stops: RouteStop[];
  total_distance: number;
  total_cost: number;
  total_weight: number;
}

export interface RouteResponse {
  express: RouteOption;
  economic: RouteOption;
  strategic: RouteOption;
}

export interface RouteRequest {
  vehicle_id: string;
  package_ids: string[];
  hub_ids?: string[];
}

export interface ApiError {
  error_code: string;
  message: string;
  details?: Record<string, unknown>;
}
