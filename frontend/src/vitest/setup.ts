import "@testing-library/jest-dom";
import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import ptBR from "../i18n/locales/pt-BR.json";

class ResizeObserverMock {
  observe() {}
  unobserve() {}
  disconnect() {}
}

(globalThis as unknown as Record<string, unknown>).ResizeObserver =
  ResizeObserverMock;

if (!i18n.isInitialized) {
  i18n.use(initReactI18next).init({
    resources: { "pt-BR": { translation: ptBR } },
    lng: "pt-BR",
    fallbackLng: "pt-BR",
    interpolation: { escapeValue: false },
  });
}
