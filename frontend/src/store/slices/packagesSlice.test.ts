import { describe, it, expect } from "vitest";
import packagesReducer, {
  fetchPackages,
  addPackage,
  removePackage,
  type PackagesState,
} from "./packagesSlice";
import type { Package, PackageCreate } from "../../types";

const mockPkg: Package = {
  id: "pkg-1",
  recipient_name: "Ana",
  x: 1,
  y: 2,
  weight: 5,
  access_cost: 0,
  deleted: false,
  created_at: "2026-01-01T00:00:00Z",
};
const mockCreate: PackageCreate = {
  recipient_name: "Ana",
  x: 1,
  y: 2,
  weight: 5,
};

describe("packagesSlice", () => {
  const initial: PackagesState = { items: [], loading: false, error: null };

  it("retorna estado inicial", () => {
    expect(packagesReducer(undefined, { type: "@@INIT" })).toEqual(initial);
  });

  it("fetchPackages.pending → loading=true", () => {
    const next = packagesReducer(initial, fetchPackages.pending(""));
    expect(next.loading).toBe(true);
    expect(next.error).toBeNull();
  });

  it("fetchPackages.fulfilled → items preenchidos", () => {
    const action = fetchPackages.fulfilled([mockPkg], "");
    const next = packagesReducer(initial, action);
    expect(next.loading).toBe(false);
    expect(next.items).toHaveLength(1);
    expect(next.items[0].id).toBe("pkg-1");
  });

  it("fetchPackages.rejected → error preenchido", () => {
    const action = fetchPackages.rejected(new Error("network"), "");
    const next = packagesReducer(initial, action);
    expect(next.loading).toBe(false);
    expect(next.error).toBe("network");
  });

  it('fetchPackages.rejected sem Error → RTK define "Rejected" como mensagem', () => {
    const action = fetchPackages.rejected(null, "");
    const next = packagesReducer(initial, action);
    expect(next.error).toBe("Rejected");
  });

  it("addPackage.fulfilled → item adicionado à lista", () => {
    const action = addPackage.fulfilled(mockPkg, "", mockCreate);
    const next = packagesReducer(initial, action);
    expect(next.items).toHaveLength(1);
    expect(next.items[0].recipient_name).toBe("Ana");
  });

  it("removePackage.fulfilled → item removido da lista", () => {
    const state: PackagesState = {
      items: [mockPkg],
      loading: false,
      error: null,
    };
    const action = removePackage.fulfilled("pkg-1", "", "pkg-1");
    const next = packagesReducer(state, action);
    expect(next.items).toHaveLength(0);
  });

  it("removePackage.fulfilled com id inexistente → lista inalterada", () => {
    const state: PackagesState = {
      items: [mockPkg],
      loading: false,
      error: null,
    };
    const action = removePackage.fulfilled(
      "does-not-exist",
      "",
      "does-not-exist",
    );
    const next = packagesReducer(state, action);
    expect(next.items).toHaveLength(1);
  });
});
