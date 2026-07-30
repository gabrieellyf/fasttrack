import { useNavigate } from "react-router-dom";
import styled, { keyframes } from "styled-components";
import {
  Navigation,
  Package,
  Truck,
  Warehouse,
  ArrowRight,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import { media } from "../../styles/theme";

const FEATURES = [
  {
    key: "routing" as const,
    path: "/routing",
    Icon: Navigation,
    color: "#2563eb",
    shadow: "0 8px 24px rgba(37,99,235,0.25)",
  },
  {
    key: "packages" as const,
    path: "/packages",
    Icon: Package,
    color: "#16a34a",
    shadow: "0 8px 24px rgba(22,163,74,0.25)",
  },
  {
    key: "vehicles" as const,
    path: "/vehicles",
    Icon: Truck,
    color: "#f59e0b",
    shadow: "0 8px 24px rgba(245,158,11,0.25)",
  },
  {
    key: "hubs" as const,
    path: "/hubs",
    Icon: Warehouse,
    color: "#8b5cf6",
    shadow: "0 8px 24px rgba(139,92,246,0.25)",
  },
] as const;

const slideUp = keyframes`
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
`;

/**
 * Central Hub dashboard — entry point displaying all available features as cards.
 */
export function HubCentral() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <Container id="main-content" tabIndex={-1}>
      <PageTitle>{t("hub.title")}</PageTitle>
      <Subtitle>{t("hub.subtitle")}</Subtitle>
      <Grid role="list">
        {FEATURES.map(({ key, path, Icon, color, shadow }, index) => {
          const descId = `hub-card-desc-${key}`;
          return (
            <FeatureCard
              key={key}
              role="listitem"
              onClick={() => navigate(path)}
              $accentColor={color}
              $shadow={shadow}
              $index={index}
              tabIndex={0}
              aria-label={t(`nav.${key}`)}
              aria-describedby={descId}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") navigate(path);
              }}
            >
              <ArrowIndicator aria-hidden="true">
                <ArrowRight size={18} />
              </ArrowIndicator>
              <IconWrapper $color={color} aria-hidden="true">
                <Icon size={28} color="#fff" />
              </IconWrapper>
              <CardTitle>{t(`nav.${key}`)}</CardTitle>
              <CardDesc id={descId}>{t(`hub.${key}Desc`)}</CardDesc>
            </FeatureCard>
          );
        })}
      </Grid>
    </Container>
  );
}

const Container = styled.main`
  flex: 1;
  padding: ${({ theme }) => theme.spacing[8]};
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;

  @media (max-width: 767px) {
    padding: ${({ theme }) => theme.spacing[5]}
      ${({ theme }) => theme.spacing[4]};
  }

  &:focus {
    outline: none;
  }
`;

const PageTitle = styled.h1`
  font-size: ${({ theme }) => theme.typography.fontSizes["3xl"]};
  font-weight: ${({ theme }) => theme.typography.fontWeights.extrabold};
  margin-bottom: ${({ theme }) => theme.spacing[1]};
`;

const Subtitle = styled.p`
  color: ${({ theme }) => theme.colors.textMuted};
  font-size: ${({ theme }) => theme.typography.fontSizes.base};
  margin-bottom: ${({ theme }) => theme.spacing[8]};
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: ${({ theme }) => theme.spacing[5]};

  ${media.sm} {
    grid-template-columns: repeat(2, 1fr);
  }
  ${media.lg} {
    grid-template-columns: repeat(4, 1fr);
  }
`;

const FeatureCard = styled.article<{
  $accentColor: string;
  $shadow: string;
  $index: number;
}>`
  background: ${({ theme }) => theme.colors.surface};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.lg};
  padding: ${({ theme }) => theme.spacing[6]};
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition:
    transform 0.22s ease,
    border-color 0.22s ease,
    box-shadow 0.22s ease;
  box-shadow: ${({ theme }) => theme.shadows.md};
  animation: ${slideUp} 0.3s ease-out both;
  animation-delay: ${({ $index }) => $index * 60}ms;

  &:hover,
  &:focus-visible {
    transform: translateY(-4px);
    border-color: ${({ $accentColor }) => $accentColor};
    box-shadow: ${({ $shadow }) => $shadow};
    outline: none;
  }
`;

const ArrowIndicator = styled.span`
  position: absolute;
  top: ${({ theme }) => theme.spacing[5]};
  right: ${({ theme }) => theme.spacing[5]};
  color: ${({ theme }) => theme.colors.border};
  opacity: 0;
  transform: translateX(-4px);
  transition:
    opacity 0.2s,
    transform 0.2s;

  ${FeatureCard}:hover &, ${FeatureCard}:focus-visible & {
    opacity: 1;
    transform: translateX(0);
    color: ${({ theme }) => theme.colors.textMuted};
  }
`;

const IconWrapper = styled.div<{ $color: string }>`
  width: 52px;
  height: 52px;
  border-radius: ${({ theme }) => theme.radius.lg};
  background: ${({ $color }) => $color};
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: ${({ theme }) => theme.spacing[4]};
`;

const CardTitle = styled.h3`
  font-size: ${({ theme }) => theme.typography.fontSizes.lg};
  font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
  margin-bottom: ${({ theme }) => theme.spacing[2]};
`;

const CardDesc = styled.p`
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textMuted};
  line-height: ${({ theme }) => theme.typography.lineHeights.relaxed};
`;
