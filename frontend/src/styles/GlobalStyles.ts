import { createGlobalStyle, keyframes } from "styled-components";

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
`;

export const GlobalStyles = createGlobalStyle`
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  html {
    font-size: 16px;
    -webkit-text-size-adjust: 100%;
    scroll-behavior: smooth;
  }

  body {
    font-family: ${({ theme }) => theme.typography.fontFamily};
    font-size: ${({ theme }) => theme.typography.fontSizes.base};
    font-weight: ${({ theme }) => theme.typography.fontWeights.regular};
    line-height: ${({ theme }) => theme.typography.lineHeights.normal};
    background-color: ${({ theme }) => theme.colors.bg};
    color: ${({ theme }) => theme.colors.text};
    transition: background-color 0.25s ease, color 0.25s ease;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    min-height: 100vh;
  }

  h1, h2, h3, h4, h5, h6 {
    font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    line-height: ${({ theme }) => theme.typography.lineHeights.tight};
    color: ${({ theme }) => theme.colors.text};
  }

  h1 { font-size: ${({ theme }) => theme.typography.fontSizes["3xl"]}; }
  h2 { font-size: ${({ theme }) => theme.typography.fontSizes["2xl"]}; }
  h3 { font-size: ${({ theme }) => theme.typography.fontSizes.xl}; }

  a {
    color: ${({ theme }) => theme.colors.brand[500]};
    text-decoration: none;
    &:hover { text-decoration: underline; }
  }

  button {
    font-family: inherit;
    cursor: pointer;
    border: none;
    background: none;
    &:disabled { cursor: not-allowed; opacity: 0.5; }
  }

    :focus-visible {
    outline: 2px solid ${({ theme }) => theme.colors.borderFocus};
    outline-offset: 2px;
    border-radius: ${({ theme }) => theme.radius.sm};
  }

    .skip-link {
    position: absolute;
    top: -100px;
    left: ${({ theme }) => theme.spacing[4]};
    z-index: 9999;
    background: ${({ theme }) => theme.colors.brand[500]};
    color: #fff;
    padding: ${({ theme }) => theme.spacing[2]} ${({ theme }) => theme.spacing[4]};
    border-radius: 0 0 ${({ theme }) => theme.radius.md} ${({ theme }) => theme.radius.md};
    font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
    font-size: ${({ theme }) => theme.typography.fontSizes.sm};
    text-decoration: none;
    transition: top 0.2s;

    &:focus {
      top: 0;
      outline: none;
    }
  }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb {
    background: ${({ theme }) => theme.colors.border};
    border-radius: ${({ theme }) => theme.radius.full};
  }
  ::-webkit-scrollbar-thumb:hover {
    background: ${({ theme }) => theme.colors.textMuted};
  }

    ::selection {
    background: ${({ theme }) => theme.colors.brand[100]};
    color: ${({ theme }) => theme.colors.brand[700]};
  }

  img, svg { display: block; max-width: 100%; }

    #root > * {
    animation: ${fadeIn} 0.2s ease-out;
  }

    @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }

    *, *::before, *::after {
    transition-property: background-color, border-color, color;
    transition-duration: 0.2s;
    transition-timing-function: ease;
  }
`;
