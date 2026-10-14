import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import App from "./App";

describe("DeployLab", () => {
  it("shows the GitOps release path and runtime stack", () => {
    render(<App />);

    expect(screen.getByRole("heading", { name: /from commit to cluster/i })).toBeInTheDocument();
    expect(screen.getByText("Argo CD")).toBeInTheDocument();
    expect(screen.getByText("K3s on Amazon EC2")).toBeInTheDocument();
    expect(screen.getByText(/not runtime telemetry/i)).toBeInTheDocument();
  });
});
