import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["src/vitest/setup.ts"],
    coverage: {
      provider: "istanbul",
      reporter: ["text", "lcov", "html"],
      exclude: [
        "src/main.tsx",
        "src/vite-env.d.ts",
        "src/vitest/**",
        "**/*.d.ts",
        "**/index.ts",
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
});
