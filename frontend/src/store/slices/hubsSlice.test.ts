import { describe, it, expect } from "vitest";
import hubsReducer, { fetchHubs, type HubsState } from "./hubsSlice";
import type { Hub } from "../../types";

const mockHub: Hub = {
  id: "h-1",
  name: "Hub Central",
  x: 0,
  y: 0,
  is_central: true,
  deleted: false,
  created_at: "2026-01-01T00:00:00Z",
};

describe("hubsSlice", () => {
  const initial: HubsState = { items: [], loading: false, error: null };

  it("retorna estado inicial", () => {
    expect(hubsReducer(undefined, { type: "@@INIT" })).toEqual(initial);
  });

  it("fetchHubs.pending → loading=true", () => {
    const next = hubsReducer(initial, fetchHubs.pending(""));
    expect(next.loading).toBe(true);
    expect(next.error).toBeNull();
  });

  it("fetchHubs.fulfilled → items preenchidos", () => {
    const action = fetchHubs.fulfilled([mockHub], "");
    const next = hubsReducer(initial, action);
    expect(next.loading).toBe(false);
    expect(next.items).toHaveLength(1);
    expect(next.items[0].name).toBe("Hub Central");
  });

  it("fetchHubs.rejected → error preenchido", () => {
    const action = fetchHubs.rejected(new Error("sem rede"), "");
    const next = hubsReducer(initial, action);
    expect(next.loading).toBe(false);
    expect(next.error).toBe("sem rede");
  });

  it('fetchHubs.rejected sem Error → RTK define "Rejected" como mensagem', () => {
    const action = fetchHubs.rejected(null, "");
    const next = hubsReducer(initial, action);
    expect(next.error).toBe("Rejected");
  });
});
