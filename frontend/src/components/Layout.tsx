import { useState, useCallback } from "react";
import { Outlet, useLocation } from "react-router-dom";
import styled from "styled-components";
import { useTranslation } from "react-i18next";
import { Header } from "./Header";
import { Drawer } from "./Drawer";

const ROUTE_TITLE_KEYS: Record<
  string,
  "routing" | "packages" | "vehicles" | "hubs"
> = {
  "/routing": "routing",
  "/packages": "packages",
  "/vehicles": "vehicles",
  "/hubs": "hubs",
};

export function HubLayout() {
  return (
    <PageWrapper>
      <a href="#main-content" className="skip-link">
        Ir para o conteúdo
      </a>
      <Header />
      <Outlet />
    </PageWrapper>
  );
}

export function FeatureLayout() {
  const { t } = useTranslation();
  const { pathname } = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleMenuToggle = useCallback(() => setMobileOpen((v) => !v), []);
  const handleMobileClose = useCallback(() => setMobileOpen(false), []);

  const titleKey = ROUTE_TITLE_KEYS[pathname];

  return (
    <PageWrapper>
      <a href="#main-content" className="skip-link">
        Ir para o conteúdo
      </a>
      <Header onMenuToggle={handleMenuToggle} />
      <BodyArea>
        <Drawer mobileOpen={mobileOpen} onMobileClose={handleMobileClose} />
        <MainArea id="main-content" tabIndex={-1}>
          {titleKey && (
            <Breadcrumb aria-label="breadcrumb">
              <BreadcrumbItem href="/">{t("hub.title")}</BreadcrumbItem>
              <BreadcrumbSep aria-hidden="true">/</BreadcrumbSep>
              <BreadcrumbCurrent aria-current="page">
                {t(`nav.${titleKey}`)}
              </BreadcrumbCurrent>
            </Breadcrumb>
          )}
          <Outlet />
        </MainArea>
      </BodyArea>
    </PageWrapper>
  );
}

const PageWrapper = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: ${({ theme }) => theme.colors.bg};
`;

const BodyArea = styled.div`
  display: flex;
  flex: 1;
  min-height: 0;
  overflow: hidden;
`;

const MainArea = styled.main<{ id?: string; tabIndex?: number }>`
  flex: 1;
  overflow: auto;
  padding: ${({ theme }) => theme.spacing[6]} ${({ theme }) => theme.spacing[8]};

  @media (max-width: 767px) {
    padding: ${({ theme }) => theme.spacing[4]}
      ${({ theme }) => theme.spacing[4]};
  }
`;

const Breadcrumb = styled.nav`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[2]};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textMuted};
  margin-bottom: ${({ theme }) => theme.spacing[4]};
`;

const BreadcrumbItem = styled.a`
  color: ${({ theme }) => theme.colors.textMuted};
  text-decoration: none;
  transition: color 0.18s;

  &:hover {
    color: ${({ theme }) => theme.colors.brand[500]};
    text-decoration: none;
  }
`;

const BreadcrumbSep = styled.span`
  color: ${({ theme }) => theme.colors.border};
`;

const BreadcrumbCurrent = styled.span`
  color: ${({ theme }) => theme.colors.text};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
`;
