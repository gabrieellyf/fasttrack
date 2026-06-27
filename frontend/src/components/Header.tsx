import styled from "styled-components";
import { Truck, Sun, Moon, Menu } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useThemeContext } from "../contexts/ThemeContext";
import { media } from "../styles/theme";

interface HeaderProps {
  onMenuToggle?: () => void;
}

export function Header({ onMenuToggle }: HeaderProps) {
  const { mode, toggle } = useThemeContext();
  const { t, i18n } = useTranslation();

  const isDark = mode === "dark";
  const currentLang = i18n.language.startsWith("en") ? "en" : "pt-BR";

  return (
    <Root>
      {onMenuToggle && (
        <HamburgerBtn onClick={onMenuToggle} aria-label="Toggle navigation">
          <Menu size={20} aria-hidden="true" />
        </HamburgerBtn>
      )}

      <LogoLink href="/" aria-label="FastTrack — Home">
        <Truck size={26} color="currentColor" aria-hidden="true" />
        <LogoText>FastTrack</LogoText>
      </LogoLink>

      <Spacer />

      <Controls>
        <LangPill role="group" aria-label={t("header.language")}>
          <LangBtn
            $active={currentLang === "pt-BR"}
            onClick={() => i18n.changeLanguage("pt-BR")}
            aria-pressed={currentLang === "pt-BR"}
          >
            PT
          </LangBtn>
          <LangSep aria-hidden="true" />
          <LangBtn
            $active={currentLang === "en"}
            onClick={() => i18n.changeLanguage("en")}
            aria-pressed={currentLang === "en"}
          >
            EN
          </LangBtn>
        </LangPill>

        <ThemeBtn
          onClick={toggle}
          aria-label={t("header.theme.toggle")}
          title={isDark ? t("header.theme.light") : t("header.theme.dark")}
        >
          {isDark ? (
            <Sun size={18} aria-hidden="true" />
          ) : (
            <Moon size={18} aria-hidden="true" />
          )}
          <ThemeLabel>
            {isDark ? t("header.theme.light") : t("header.theme.dark")}
          </ThemeLabel>
        </ThemeBtn>
      </Controls>
    </Root>
  );
}

const Root = styled.header`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[3]};
  padding: 0 ${({ theme }) => theme.spacing[6]};
  height: 62px;
  background: ${({ theme }) => theme.colors.surface};
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
  box-shadow: ${({ theme }) => theme.shadows.sm};
  position: sticky;
  top: 0;
  z-index: ${({ theme }) => theme.zIndices.drawer};
  flex-shrink: 0;
`;

const HamburgerBtn = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: ${({ theme }) => theme.radius.md};
  color: ${({ theme }) => theme.colors.textMuted};
  transition:
    background 0.18s,
    color 0.18s;

  &:hover {
    background: ${({ theme }) => theme.colors.surface2};
    color: ${({ theme }) => theme.colors.text};
  }

  ${media.md} {
    display: none;
  }
`;

const LogoLink = styled.a`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[2]};
  color: ${({ theme }) => theme.colors.brand[500]};
  text-decoration: none;
  flex-shrink: 0;

  &:hover {
    text-decoration: none;
  }
`;

const LogoText = styled.span`
  font-weight: ${({ theme }) => theme.typography.fontWeights.extrabold};
  font-size: ${({ theme }) => theme.typography.fontSizes.xl};
  color: ${({ theme }) => theme.colors.brand[500]};
`;

const Spacer = styled.div`
  flex: 1;
`;

const Controls = styled.div`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[2]};
`;

const LangPill = styled.div`
  display: flex;
  align-items: center;
  background: ${({ theme }) => theme.colors.surface2};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.full};
  padding: 4px;
  gap: 2px;
`;

const LangBtn = styled.button<{ $active: boolean }>`
  padding: 5px 10px;
  border-radius: ${({ theme }) => theme.radius.full};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  transition:
    background 0.18s,
    color 0.18s;
  background: ${({ theme, $active }) =>
    $active ? theme.colors.brand[500] : "transparent"};
  color: ${({ theme, $active }) => ($active ? "#fff" : theme.colors.textMuted)};

  &:hover {
    color: ${({ theme, $active }) => ($active ? "#fff" : theme.colors.text)};
  }
`;

const LangSep = styled.div`
  width: 1px;
  height: 14px;
  background: ${({ theme }) => theme.colors.border};
`;

const ThemeBtn = styled.button`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[1]};
  padding: 7px 12px;
  border-radius: ${({ theme }) => theme.radius.full};
  background: ${({ theme }) => theme.colors.surface2};
  border: 1px solid ${({ theme }) => theme.colors.border};
  color: ${({ theme }) => theme.colors.text};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  transition:
    border-color 0.18s,
    color 0.18s;

  &:hover {
    border-color: ${({ theme }) => theme.colors.brand[500]};
    color: ${({ theme }) => theme.colors.brand[500]};
  }
`;

const ThemeLabel = styled.span`
  display: none;
  ${media.sm} {
    display: inline;
  }
`;
