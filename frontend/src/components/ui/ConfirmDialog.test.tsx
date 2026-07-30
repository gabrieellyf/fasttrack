import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ThemeProvider } from "styled-components";
import { lightTheme } from "../../styles/theme";
import { ConfirmDialog } from "./ConfirmDialog";

function wrap(ui: React.ReactNode) {
  return render(<ThemeProvider theme={lightTheme}>{ui}</ThemeProvider>);
}

describe("ConfirmDialog", () => {
  it("renders nothing when closed", () => {
    wrap(
      <ConfirmDialog
        isOpen={false}
        title="Remove?"
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />,
    );
    expect(screen.queryByRole("dialog")).toBeNull();
  });

  it("renders title and description when open", () => {
    wrap(
      <ConfirmDialog
        isOpen={true}
        title="Remove package?"
        description="This cannot be undone."
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />,
    );
    expect(screen.getByRole("dialog")).toBeDefined();
    expect(screen.getByText("Remove package?")).toBeDefined();
    expect(screen.getByText("This cannot be undone.")).toBeDefined();
  });

  it("calls onConfirm when confirm button is clicked", () => {
    const onConfirm = vi.fn();
    wrap(
      <ConfirmDialog
        isOpen={true}
        title="Are you sure?"
        confirmLabel="Yes"
        cancelLabel="No"
        onConfirm={onConfirm}
        onCancel={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByText("Yes"));
    expect(onConfirm).toHaveBeenCalledOnce();
  });

  it("calls onCancel when cancel button is clicked", () => {
    const onCancel = vi.fn();
    wrap(
      <ConfirmDialog
        isOpen={true}
        title="Are you sure?"
        confirmLabel="Yes"
        cancelLabel="No"
        onConfirm={vi.fn()}
        onCancel={onCancel}
      />,
    );
    fireEvent.click(screen.getByText("No"));
    expect(onCancel).toHaveBeenCalledOnce();
  });

  it("calls onCancel when overlay is clicked", () => {
    const onCancel = vi.fn();
    wrap(
      <ConfirmDialog
        isOpen={true}
        title="Are you sure?"
        onConfirm={vi.fn()}
        onCancel={onCancel}
      />,
    );
    fireEvent.click(screen.getByRole("presentation"));
    expect(onCancel).toHaveBeenCalledOnce();
  });
});
