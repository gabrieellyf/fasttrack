import { describe, it, expect } from "vitest";
import routesReducer, {
  clearRoutes,
  fetchRoutes,
  type RoutesState,
} from "./routesSlice";
import type { RouteResponse, RouteRequest } from "../../types";

const mockStop = { id: "hub", label: "Hub", x: 0, y: 0 };
const mockOption = {
  type: "express" as const,
  stops: [mockStop],
  total_distance: 10.0,
  total_cost: 15.0,
  total_weight: 5.0,
};
const mockResult: RouteResponse = {
  express: mockOption,
  economic: { ...mockOption, type: "economic" },
  strategic: { ...mockOption, type: "strategic" },
};
const mockRequest: RouteRequest = {
  vehicle_id: "v1",
  package_ids: ["p1"],
};

describe("routesSlice", () => {
  const initial: RoutesState = {
    result: null,
    loading: false,
    error: null,
    errorCode: null,
    errorDetails: null,
  };

  it("retorna estado inicial", () => {
    expect(routesReducer(undefined, { type: "@@INIT" })).toEqual(initial);
  });

  it("clearRoutes zera result e error", () => {
    const state: RoutesState = {
      result: mockResult,
      loading: false,
      error: "erro",
      errorCode: "WEIGHT_LIMIT_EXCEEDED",
      errorDetails: { total_weight: 110, max_weight: 100 },
    };
    const next = routesReducer(state, clearRoutes());
    expect(next.result).toBeNull();
    expect(next.error).toBeNull();
    expect(next.loading).toBe(false);
  });

  it("fetchRoutes.pending → loading=true, error=null", () => {
    const action = fetchRoutes.pending("", mockRequest);
    const next = routesReducer(initial, action);
    expect(next.loading).toBe(true);
    expect(next.error).toBeNull();
  });

  it("fetchRoutes.fulfilled → loading=false, result preenchido", () => {
    const action = fetchRoutes.fulfilled(mockResult, "", mockRequest);
    const next = routesReducer(initial, action);
    expect(next.loading).toBe(false);
    expect(next.result).toEqual(mockResult);
    expect(next.error).toBeNull();
  });

  it("fetchRoutes.rejected → loading=false, error preenchido", () => {
    const action = fetchRoutes.rejected(new Error("falhou"), "", mockRequest);
    const next = routesReducer(initial, action);
    expect(next.loading).toBe(false);
    expect(next.result).toBeNull();
    expect(next.error).toBe("falhou");
  });

  it('fetchRoutes.rejected without Error -> RTK sets "Rejected" as message', () => {
    const action = fetchRoutes.rejected(null, "", mockRequest);
    const next = routesReducer(initial, action);
    expect(next.error).toBe("Rejected");
  });
});
