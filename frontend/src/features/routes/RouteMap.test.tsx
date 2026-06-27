import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { ThemeProvider } from "styled-components";
import type { ReactNode } from "react";
import { lightTheme } from "../../styles/theme";
import { RouteMap } from "./RouteMap";
import type { RouteOption } from "../../types";

function wrap(ui: ReactNode) {
  return render(<ThemeProvider theme={lightTheme}>{ui}</ThemeProvider>);
}

const makeRoute = (
  type: "express" | "economic" | "strategic",
): RouteOption => ({
  type,
  stops: [
    { id: "hub", label: "Hub Central", x: 0, y: 0 },
    { id: "p1", label: "Pacote A", x: 3, y: 4 },
    { id: "hub-return", label: "Hub Central", x: 0, y: 0 },
  ],
  total_distance: 10.0,
  total_cost: 12.5,
  total_weight: 8.0,
});

const props = {
  express: makeRoute("express"),
  economic: makeRoute("economic"),
  strategic: makeRoute("strategic"),
};

describe("RouteMap", () => {
  it("renderiza a tabela de resumo", () => {
    wrap(<RouteMap {...props} />);
    expect(screen.getByText("Expressa")).toBeInTheDocument();
    expect(screen.getByText("Econômica")).toBeInTheDocument();
    expect(screen.getByText("Estratégica")).toBeInTheDocument();
  });

  it("exibe distância total na tabela", () => {
    wrap(<RouteMap {...props} />);

    const cells = screen.getAllByText("10.00 u");
    expect(cells.length).toBe(3);
  });

  it("exibe custo total na tabela", () => {
    wrap(<RouteMap {...props} />);
    const cells = screen.getAllByText("12.50");
    expect(cells.length).toBe(3);
  });

  it("exibe peso total na tabela", () => {
    wrap(<RouteMap {...props} />);
    const cells = screen.getAllByText("8.0 kg");
    expect(cells.length).toBe(3);
  });

  it("destaca linha da rota ativa com activeRoute", () => {
    wrap(<RouteMap {...props} activeRoute="express" />);

    expect(screen.getByText("Expressa")).toBeInTheDocument();
  });
});
