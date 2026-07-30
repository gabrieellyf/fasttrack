import { describe, it, expect } from "vitest";
import vehiclesReducer, {
  fetchVehicles,
  addVehicle,
  type VehiclesState,
} from "./vehiclesSlice";
import type { Vehicle, VehicleCreate } from "../../types";

const mockVehicle: Vehicle = {
  id: "v-1",
  plate: "ABC-1234",
  max_weight: 1000,
  deleted: false,
  created_at: "2026-01-01T00:00:00Z",
};
const mockCreate: VehicleCreate = { plate: "ABC-1234", max_weight: 1000 };

describe("vehiclesSlice", () => {
  const initial: VehiclesState = { items: [], loading: false, error: null };

  it("retorna estado inicial", () => {
    expect(vehiclesReducer(undefined, { type: "@@INIT" })).toEqual(initial);
  });

  it("fetchVehicles.pending → loading=true", () => {
    const next = vehiclesReducer(initial, fetchVehicles.pending(""));
    expect(next.loading).toBe(true);
  });

  it("fetchVehicles.fulfilled → items preenchidos", () => {
    const action = fetchVehicles.fulfilled([mockVehicle], "");
    const next = vehiclesReducer(initial, action);
    expect(next.items).toHaveLength(1);
    expect(next.items[0].plate).toBe("ABC-1234");
  });

  it("fetchVehicles.rejected → error preenchido", () => {
    const action = fetchVehicles.rejected(new Error("timeout"), "");
    const next = vehiclesReducer(initial, action);
    expect(next.error).toBe("timeout");
  });

  it('fetchVehicles.rejected sem Error → RTK define "Rejected" como mensagem', () => {
    const action = fetchVehicles.rejected(null, "");
    const next = vehiclesReducer(initial, action);
    expect(next.error).toBe("Rejected");
  });

  it("addVehicle.fulfilled → veículo adicionado", () => {
    const action = addVehicle.fulfilled(mockVehicle, "", mockCreate);
    const next = vehiclesReducer(initial, action);
    expect(next.items).toHaveLength(1);
  });
});
