export type ThemeMode = "light" | "dark";

const brand = {
  50: "#eff4ff",
  100: "#dbe6fe",
  200: "#bfd1fe",
  300: "#93b4fd",
  400: "#6090fb",
  500: "#2563eb",
  600: "#1d4ed8",
  700: "#1e40af",
  800: "#1e3a8a",
  900: "#1e3460",
} as const;

const strategies = {
  express: "#2563eb",
  economic: "#16a34a",
  strategic: "#f59e0b",
} as const;

const feedback = {
  success: "#16a34a",
  successBg: "#f0fdf4",
  warning: "#f59e0b",
  warningBg: "#fffbeb",
  error: "#dc2626",
  errorBg: "#fef2f2",
  info: "#0ea5e9",
  infoBg: "#f0f9ff",
} as const;

const typography = {
  fontFamily: "'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif",
  fontSizes: {
    xs: "11px",
    sm: "13px",
    base: "15px",
    lg: "17px",
    xl: "20px",
    "2xl": "24px",
    "3xl": "30px",
    "4xl": "36px",
  },
  fontWeights: {
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
  },
  lineHeights: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75,
  },
} as const;

const spacing = {
  1: "4px",
  2: "8px",
  3: "12px",
  4: "16px",
  5: "20px",
  6: "24px",
  8: "32px",
  10: "40px",
  12: "48px",
  16: "64px",
} as const;

const radius = {
  sm: "6px",
  md: "10px",
  lg: "14px",
  xl: "20px",
  full: "9999px",
} as const;

const breakpoints = {
  sm: "640px",
  md: "768px",
  lg: "1024px",
  xl: "1280px",
} as const;

export const media = {
  sm: `@media (min-width: ${breakpoints.sm})`,
  md: `@media (min-width: ${breakpoints.md})`,
  lg: `@media (min-width: ${breakpoints.lg})`,
  xl: `@media (min-width: ${breakpoints.xl})`,
} as const;

export interface AppTheme {
  mode: ThemeMode;
  colors: {
    bg: string;
    surface: string;
    surface2: string;
    border: string;
    borderFocus: string;
    text: string;
    textMuted: string;
    textInverse: string;
    brand: typeof brand;
    strategies: typeof strategies;
    feedback: typeof feedback;
    drawer: {
      bg: string;
      surface: string;
      text: string;
      textMuted: string;
      active: string;
      activeBg: string;
      border: string;
      hoverBg: string;
    };
  };
  typography: typeof typography;
  spacing: typeof spacing;
  radius: typeof radius;
  shadows: {
    sm: string;
    md: string;
    lg: string;
    brand: string;
    express: string;
    economic: string;
    strategic: string;
  };
  breakpoints: typeof breakpoints;
  zIndices: {
    drawer: number;
    overlay: number;
    modal: number;
    toast: number;
  };
}

export const lightTheme: AppTheme = {
  mode: "light",
  colors: {
    bg: "#f5f7fb",
    surface: "#ffffff",
    surface2: "#f0f3f9",
    border: "#e2e8f0",
    borderFocus: "#2563eb",
    text: "#0f172a",
    textMuted: "#64748b",
    textInverse: "#ffffff",
    brand,
    strategies,
    feedback,
    drawer: {
      bg: "#0f172a",
      surface: "#1a2640",
      text: "#cbd5e1",
      textMuted: "#4b6177",
      active: "#2563eb",
      activeBg: "rgba(37,99,235,0.15)",
      border: "#27344b",
      hoverBg: "rgba(255,255,255,0.06)",
    },
  },
  typography,
  spacing,
  radius,
  shadows: {
    sm: "0 1px 3px rgba(15,23,42,.08), 0 1px 8px rgba(15,23,42,.04)",
    md: "0 1px 3px rgba(15,23,42,.08), 0 8px 24px rgba(15,23,42,.06)",
    lg: "0 4px 6px rgba(15,23,42,.07), 0 24px 48px rgba(15,23,42,.12)",
    brand: "0 4px 14px rgba(37,99,235,.35)",
    express: "0 4px 14px rgba(37,99,235,.3)",
    economic: "0 4px 14px rgba(22,163,74,.3)",
    strategic: "0 4px 14px rgba(245,158,11,.3)",
  },
  breakpoints,
  zIndices: { drawer: 20, overlay: 30, modal: 40, toast: 50 },
};

export const darkTheme: AppTheme = {
  mode: "dark",
  colors: {
    bg: "#0b1220",
    surface: "#131c2e",
    surface2: "#1b263b",
    border: "#27344b",
    borderFocus: "#3b82f6",
    text: "#e8eef7",
    textMuted: "#93a4bd",
    textInverse: "#0f172a",
    brand,
    strategies,
    feedback,
    drawer: {
      bg: "#070d18",
      surface: "#0f1829",
      text: "#9fb0c9",
      textMuted: "#3d5268",
      active: "#3b82f6",
      activeBg: "rgba(59,130,246,0.15)",
      border: "#1c2c42",
      hoverBg: "rgba(255,255,255,0.05)",
    },
  },
  typography,
  spacing,
  radius,
  shadows: {
    sm: "0 1px 3px rgba(0,0,0,.3), 0 1px 8px rgba(0,0,0,.2)",
    md: "0 1px 3px rgba(0,0,0,.4), 0 12px 30px rgba(0,0,0,.35)",
    lg: "0 4px 6px rgba(0,0,0,.4), 0 24px 48px rgba(0,0,0,.5)",
    brand: "0 4px 14px rgba(59,130,246,.4)",
    express: "0 4px 14px rgba(59,130,246,.35)",
    economic: "0 4px 14px rgba(22,163,74,.35)",
    strategic: "0 4px 14px rgba(245,158,11,.35)",
  },
  breakpoints,
  zIndices: { drawer: 20, overlay: 30, modal: 40, toast: 50 },
};
