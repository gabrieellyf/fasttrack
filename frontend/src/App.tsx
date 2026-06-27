import { ThemeProvider } from "styled-components";
import { Toaster } from "sonner";
import { AppRouter } from "./router";
import { GlobalStyles } from "./styles/GlobalStyles";
import { lightTheme, darkTheme } from "./styles/theme";
import { ThemeContextProvider, useThemeContext } from "./contexts/ThemeContext";
import "./i18n";

function AppWithTheme() {
  const { mode } = useThemeContext();
  const theme = mode === "light" ? lightTheme : darkTheme;

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <Toaster position="top-right" richColors />
      <AppRouter />
    </ThemeProvider>
  );
}

export default function App() {
  return (
    <ThemeContextProvider>
      <AppWithTheme />
    </ThemeContextProvider>
  );
}
