import { useState, useCallback, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import styled, { css } from "styled-components";
import {
  Navigation,
  Package,
  Truck,
  Warehouse,
  Home,
  ChevronLeft,
  ChevronRight,
  X,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import { media } from "../styles/theme";

const STORAGE_KEY = "fasttrack-drawer-collapsed";

const NAV_ITEMS = [
  { key: "routing" as const, path: "/routing", Icon: Navigation },
  { key: "packages" as const, path: "/packages", Icon: Package },
  { key: "vehicles" as const, path: "/vehicles", Icon: Truck },
  { key: "hubs" as const, path: "/hubs", Icon: Warehouse },
];

interface DrawerProps {
  mobileOpen: boolean;
  onMobileClose: () => void;
}

export function Drawer({ mobileOpen, onMobileClose }: DrawerProps) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const [collapsed, setCollapsed] = useState<boolean>(() => {
    try {
      return localStorage.getItem(STORAGE_KEY) === "true";
    } catch {
      return false;
    }
  });

  const toggleCollapse = useCallback(() => {
    setCollapsed((prev) => {
      const next = !prev;
      try {
        localStorage.setItem(STORAGE_KEY, String(next));
      } catch {}
      return next;
    });
  }, []);

  const handleNav = useCallback(
    (path: string) => {
      navigate(path);
      onMobileClose();
    },
    [navigate, onMobileClose],
  );

  const handleBackToHub = useCallback(() => {
    navigate("/");
    onMobileClose();
  }, [navigate, onMobileClose]);

  useEffect(() => {
    if (!mobileOpen) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onMobileClose();
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [mobileOpen, onMobileClose]);

  return (
    <>
      {mobileOpen && <Overlay onClick={onMobileClose} aria-hidden="true" />}

      <Root
        $collapsed={collapsed}
        $mobileOpen={mobileOpen}
        role="navigation"
        aria-label="Navegação lateral"
      >
        <BackBtn onClick={handleBackToHub} title={t("nav.backToHub")}>
          <Home size={18} aria-hidden="true" />
          {!collapsed && <span>{t("nav.backToHub")}</span>}
        </BackBtn>

        <NavList>
          {NAV_ITEMS.map(({ key, path, Icon }) => {
            const isActive =
              pathname === path || pathname.startsWith(path + "/");
            return (
              <NavItem
                key={key}
                $active={isActive}
                onClick={() => handleNav(path)}
                title={collapsed ? t(`nav.${key}`) : undefined}
                aria-current={isActive ? "page" : undefined}
              >
                <Icon size={20} aria-hidden="true" />
                {!collapsed && <NavLabel>{t(`nav.${key}`)}</NavLabel>}
              </NavItem>
            );
          })}
        </NavList>

        <DrawerFoot>
          {mobileOpen && (
            <CloseBtn onClick={onMobileClose} aria-label="Fechar menu">
              <X size={18} aria-hidden="true" />
              <span>Fechar</span>
            </CloseBtn>
          )}
          <CollapseBtn
            onClick={toggleCollapse}
            aria-label={collapsed ? t("nav.expand") : t("nav.collapse")}
          >
            {collapsed ? (
              <ChevronRight size={18} aria-hidden="true" />
            ) : (
              <ChevronLeft size={18} aria-hidden="true" />
            )}
            {!collapsed && <span>{t("nav.collapse")}</span>}
          </CollapseBtn>
        </DrawerFoot>
      </Root>
    </>
  );
}

const Overlay = styled.div`
  display: none;

  @media (max-width: 767px) {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: ${({ theme }) => theme.zIndices.overlay};
  }
`;

const Root = styled.aside<{ $collapsed: boolean; $mobileOpen: boolean }>`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing[1]};
  background: ${({ theme }) => theme.colors.drawer.bg};
  border-right: 1px solid ${({ theme }) => theme.colors.drawer.border};
  padding: ${({ theme }) => theme.spacing[4]} ${({ theme }) => theme.spacing[3]};
  transition:
    width 0.25s ease,
    transform 0.25s ease;
  overflow: hidden;
  flex-shrink: 0;

  ${media.md} {
    position: relative;
    width: ${({ $collapsed }) => ($collapsed ? "68px" : "248px")};
    transform: none;
    z-index: auto;
  }

  @media (max-width: 767px) {
    position: fixed;
    top: 62px;
    left: 0;
    bottom: 0;
    width: 256px;
    z-index: ${({ theme }) => theme.zIndices.drawer};
    transform: ${({ $mobileOpen }) =>
      $mobileOpen ? "translateX(0)" : "translateX(-100%)"};
  }
`;

const baseNavItem = css`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[3]};
  padding: ${({ theme }) => theme.spacing[3]};
  border-radius: ${({ theme }) => theme.radius.md};
  cursor: pointer;
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  white-space: nowrap;
  overflow: hidden;
  transition:
    background 0.18s,
    color 0.18s;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
`;

const BackBtn = styled.button`
  ${baseNavItem}
  color: ${({ theme }) => theme.colors.drawer.text};
  border: 1px dashed ${({ theme }) => theme.colors.drawer.border};
  margin-bottom: ${({ theme }) => theme.spacing[2]};

  &:hover {
    background: ${({ theme }) => theme.colors.drawer.hoverBg};
    color: #fff;
  }
`;

const NavList = styled.ul`
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing[1]};
  flex: 1;
`;

const NavItem = styled.li<{ $active: boolean }>`
  ${baseNavItem}
  color: ${({ theme, $active }) =>
    $active ? "#fff" : theme.colors.drawer.text};
  background: ${({ theme, $active }) =>
    $active ? theme.colors.drawer.active : "transparent"};
  box-shadow: ${({ theme, $active }) =>
    $active ? theme.shadows.brand : "none"};

  &:hover {
    background: ${({ theme, $active }) =>
      $active ? theme.colors.drawer.active : theme.colors.drawer.hoverBg};
    color: ${({ $active }) => ($active ? "#fff" : "#fff")};
  }
`;

const NavLabel = styled.span`
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
`;

const DrawerFoot = styled.div`
  margin-top: auto;
  padding-top: ${({ theme }) => theme.spacing[2]};
  border-top: 1px solid ${({ theme }) => theme.colors.drawer.border};
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing[1]};
`;

const CollapseBtn = styled.button`
  ${baseNavItem}
  color: ${({ theme }) => theme.colors.drawer.text};
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};

  &:hover {
    background: ${({ theme }) => theme.colors.drawer.hoverBg};
    color: #fff;
  }
`;

const CloseBtn = styled.button`
  ${baseNavItem}
  color: ${({ theme }) => theme.colors.drawer.text};

  &:hover {
    background: ${({ theme }) => theme.colors.drawer.hoverBg};
    color: #fff;
  }

  ${media.md} {
    display: none;
  }
`;
