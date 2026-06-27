import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import styled from "styled-components";
import {
  Zap,
  TrendingDown,
  GitMerge,
  AlertTriangle,
  ChevronRight,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import type { AppDispatch, RootState } from "../../store";
import { fetchPackages } from "../../store/slices/packagesSlice";
import { fetchVehicles } from "../../store/slices/vehiclesSlice";
import { fetchRoutes, clearRoutes } from "../../store/slices/routesSlice";
import { RouteMap } from "./RouteMap";
import { PageHeader } from "../../components/ui/PageHeader";
import { SkeletonBox } from "../../components/ui/Skeleton";
import { media } from "../../styles/theme";
import type { RouteOption, RouteResponse } from "../../types";

type RouteType = "express" | "economic" | "strategic";

const STRATEGY_ICONS = {
  express: Zap,
  economic: TrendingDown,
  strategic: GitMerge,
};

function getBadges(
  result: RouteResponse,
): Record<RouteType, ("fastest" | "cheapest")[]> {
  const types: RouteType[] = ["express", "economic", "strategic"];
  const minDist = Math.min(...types.map((t) => result[t].total_distance));
  const minCost = Math.min(...types.map((t) => result[t].total_cost));
  const badges: Record<RouteType, ("fastest" | "cheapest")[]> = {
    express: [],
    economic: [],
    strategic: [],
  };
  types.forEach((type) => {
    if (result[type].total_distance === minDist) badges[type].push("fastest");
    if (result[type].total_cost === minCost) badges[type].push("cheapest");
  });
  return badges;
}

export function RouteCalculator() {
  const dispatch = useDispatch<AppDispatch>();
  const { t } = useTranslation();
  const { items: packages, loading: pkgLoading } = useSelector(
    (s: RootState) => s.packages,
  );
  const { items: vehicles, loading: vhLoading } = useSelector(
    (s: RootState) => s.vehicles,
  );
  const { result, loading, error, errorCode, errorDetails } = useSelector(
    (s: RootState) => s.routes,
  );

  const [vehicleId, setVehicleId] = useState("");
  const [selectedPackages, setSelectedPackages] = useState<Set<string>>(
    new Set(),
  );
  const [activeRoute, setActiveRoute] = useState<RouteType | undefined>(
    undefined,
  );

  useEffect(() => {
    dispatch(fetchPackages());
    dispatch(fetchVehicles());
    return () => {
      dispatch(clearRoutes());
    };
  }, [dispatch]);

  function togglePackage(id: string) {
    setSelectedPackages((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!vehicleId || selectedPackages.size === 0) return;
    setActiveRoute(undefined);
    dispatch(
      fetchRoutes({
        vehicle_id: vehicleId,
        package_ids: [...selectedPackages],
      }),
    );
  }

  const pkgCount = selectedPackages.size;
  const badges = result ? getBadges(result) : null;

  const strategyColors: Record<RouteType, string> = {
    express: "#2563eb",
    economic: "#16a34a",
    strategic: "#f59e0b",
  };

  return (
    <Container>
      <PageHeader title={t("routing.title")} subtitle={t("routing.subtitle")} />

      <FormCard onSubmit={handleSubmit}>
        {}
        <FormGroup>
          <Label htmlFor="vehicle-select">{t("routing.vehicle")}</Label>
          <Select
            id="vehicle-select"
            value={vehicleId}
            onChange={(e) => setVehicleId(e.target.value)}
            required
          >
            <option value="">
              {vhLoading
                ? t("routing.vehicleLoading")
                : t("routing.vehiclePlaceholder")}
            </option>
            {vehicles.map((v) => (
              <option key={v.id} value={v.id}>
                {v.plate} — cap. {v.max_weight} kg
              </option>
            ))}
          </Select>
        </FormGroup>

        {/* Package selector */}
        <FormGroup>
          <Label>
            {t("routing.packages")}{" "}
            <CountBadge>
              {t(`routing.packagesSelected`, { count: pkgCount })}
            </CountBadge>
          </Label>
          <PackageScroll>
            {pkgLoading && (
              <LoadingMsg>{t("routing.packagesLoading")}</LoadingMsg>
            )}
            {!pkgLoading && packages.length === 0 && (
              <LoadingMsg>{t("routing.packagesEmpty")}</LoadingMsg>
            )}
            {packages.map((p) => (
              <PackageCheckItem key={p.id}>
                <input
                  type="checkbox"
                  id={`pkg-${p.id}`}
                  checked={selectedPackages.has(p.id)}
                  onChange={() => togglePackage(p.id)}
                />
                <label htmlFor={`pkg-${p.id}`}>
                  {p.recipient_name} — ({p.x}, {p.y}) — {p.weight} kg — acesso:{" "}
                  {p.access_cost}
                </label>
              </PackageCheckItem>
            ))}
          </PackageScroll>
        </FormGroup>

        <SubmitBtn
          type="submit"
          disabled={loading || !vehicleId || selectedPackages.size === 0}
        >
          {loading ? t("routing.calculating") : t("routing.calculate")}
        </SubmitBtn>
      </FormCard>

      {}
      {errorCode === "WEIGHT_LIMIT_EXCEEDED" && errorDetails && (
        <WeightBanner role="alert">
          <AlertTriangle size={20} aria-hidden="true" />
          <div>
            <strong>
              {t("routing.errors.weightLimit", {
                total: errorDetails.total_weight?.toFixed(2),
                max: errorDetails.max_weight?.toFixed(2),
              })}
            </strong>
          </div>
        </WeightBanner>
      )}

      {}
      {error && errorCode !== "WEIGHT_LIMIT_EXCEEDED" && (
        <ErrorBanner role="alert">{error}</ErrorBanner>
      )}

      {}
      {loading && (
        <ResultSection aria-live="polite" aria-busy="true">
          <CardsGrid>
            {[0, 1, 2].map((i) => (
              <SkeletonCard key={i}>
                <SkeletonBox $height="20px" $width="60%" />
                <SkeletonBox $height="14px" $width="80%" />
                <SkeletonBox $height="14px" $width="70%" />
                <SkeletonBox $height="14px" $width="75%" />
              </SkeletonCard>
            ))}
          </CardsGrid>
        </ResultSection>
      )}

      {}
      {result && !loading && (
        <ResultSection aria-live="polite" aria-label={t("routing.result")}>
          {}
          <TabBar role="tablist" aria-label={t("routing.result")}>
            <Tab
              role="tab"
              aria-selected={activeRoute == null}
              $active={activeRoute == null}
              onClick={() => setActiveRoute(undefined)}
            >
              {t("routing.compareAll")}
            </Tab>
            {(["express", "economic", "strategic"] as RouteType[]).map(
              (type) => (
                <Tab
                  key={type}
                  role="tab"
                  aria-selected={activeRoute === type}
                  $active={activeRoute === type}
                  $color={strategyColors[type]}
                  onClick={() =>
                    setActiveRoute(activeRoute === type ? undefined : type)
                  }
                >
                  {t(`routing.strategies.${type}`)}
                </Tab>
              ),
            )}
          </TabBar>

          {}
          <CardsGrid>
            {(["express", "economic", "strategic"] as RouteType[]).map(
              (type) => {
                const route: RouteOption = result[type];
                const Icon = STRATEGY_ICONS[type];
                const isSelected = activeRoute === type;
                const cardBadges = badges?.[type] ?? [];

                return (
                  <RouteCard
                    key={type}
                    $color={strategyColors[type]}
                    $selected={isSelected}
                    onClick={() =>
                      setActiveRoute(isSelected ? undefined : type)
                    }
                    role="button"
                    aria-pressed={isSelected}
                    tabIndex={0}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" || e.key === " ")
                        setActiveRoute(isSelected ? undefined : type);
                    }}
                  >
                    <CardHeader>
                      <CardIcon $color={strategyColors[type]}>
                        <Icon size={18} color="#fff" aria-hidden="true" />
                      </CardIcon>
                      <CardTitle>{t(`routing.strategies.${type}`)}</CardTitle>
                      {isSelected && (
                        <SelectedIndicator aria-hidden="true">
                          <ChevronRight size={16} />
                        </SelectedIndicator>
                      )}
                    </CardHeader>

                    {cardBadges.length > 0 && (
                      <BadgeRow>
                        {cardBadges.includes("fastest") && (
                          <Badge $color={strategyColors.express}>
                            {t("routing.badges.fastest")}
                          </Badge>
                        )}
                        {cardBadges.includes("cheapest") && (
                          <Badge $color={strategyColors.economic}>
                            {t("routing.badges.cheapest")}
                          </Badge>
                        )}
                      </BadgeRow>
                    )}

                    <MetricList>
                      <MetricRow>
                        <MetricLabel>
                          {t("routing.metrics.totalDistance")}
                        </MetricLabel>
                        <MetricValue>
                          {route.total_distance.toFixed(2)}{" "}
                          {t("routing.metrics.distanceUnit")}
                        </MetricValue>
                      </MetricRow>
                      <MetricRow>
                        <MetricLabel>
                          {t("routing.metrics.totalCost")}
                        </MetricLabel>
                        <MetricValue>{route.total_cost.toFixed(2)}</MetricValue>
                      </MetricRow>
                      <MetricRow $last>
                        <MetricLabel>
                          {t("routing.metrics.totalWeight")}
                        </MetricLabel>
                        <MetricValue>
                          {route.total_weight.toFixed(1)}{" "}
                          {t("routing.metrics.weightUnit")}
                        </MetricValue>
                      </MetricRow>
                    </MetricList>
                  </RouteCard>
                );
              },
            )}
          </CardsGrid>

          {}
          <RouteMap
            express={result.express}
            economic={result.economic}
            strategic={result.strategic}
            activeRoute={activeRoute}
          />

          {}
          {activeRoute && (
            <StopSequence>
              <StopTitle>
                {t("routing.stopSequence")} —{" "}
                {t(`routing.strategies.${activeRoute}`)}
              </StopTitle>
              <StopList>
                {result[activeRoute].stops.map((s, i) => (
                  <StopItem key={i}>
                    <StopNum>{i + 1}</StopNum>
                    <div>
                      <StopLabel>{s.label}</StopLabel>
                      <StopCoords>
                        ({s.x}, {s.y})
                      </StopCoords>
                    </div>
                  </StopItem>
                ))}
              </StopList>
            </StopSequence>
          )}
        </ResultSection>
      )}
    </Container>
  );
}

const Container = styled.div`
  max-width: 1000px;
`;

const FormCard = styled.form`
  background: ${({ theme }) => theme.colors.surface};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.lg};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.sm};
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing[5]};
  margin-bottom: ${({ theme }) => theme.spacing[6]};
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing[2]};
`;

const Label = styled.label`
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  color: ${({ theme }) => theme.colors.text};
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[2]};
`;

const CountBadge = styled.span`
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeights.medium};
  color: ${({ theme }) => theme.colors.textMuted};
  background: ${({ theme }) => theme.colors.surface2};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.full};
  padding: 2px 8px;
`;

const Select = styled.select`
  width: 100%;
  padding: 10px 14px;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.md};
  background: ${({ theme }) => theme.colors.surface};
  color: ${({ theme }) => theme.colors.text};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  font-family: inherit;
  transition: border-color 0.18s;
  cursor: pointer;

  &:focus {
    border-color: ${({ theme }) => theme.colors.borderFocus};
    outline: none;
  }

  ${media.md} {
    max-width: 400px;
  }
`;

const PackageScroll = styled.div`
  max-height: 220px;
  overflow-y: auto;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.md};
  padding: ${({ theme }) => theme.spacing[2]};
  background: ${({ theme }) => theme.colors.surface2};
`;

const PackageCheckItem = styled.div`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[2]};
  padding: ${({ theme }) => theme.spacing[2]} ${({ theme }) => theme.spacing[2]};
  border-radius: ${({ theme }) => theme.radius.sm};
  cursor: pointer;
  transition: background 0.15s;

  &:hover {
    background: ${({ theme }) => theme.colors.surface};
  }

  label {
    font-size: ${({ theme }) => theme.typography.fontSizes.sm};
    color: ${({ theme }) => theme.colors.text};
    cursor: pointer;
    line-height: 1.4;
  }

  input[type="checkbox"] {
    cursor: pointer;
    accent-color: ${({ theme }) => theme.colors.brand[500]};
  }
`;

const LoadingMsg = styled.p`
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textMuted};
  padding: ${({ theme }) => theme.spacing[3]};
`;

const SubmitBtn = styled.button`
  align-self: flex-start;
  padding: 11px 28px;
  background: ${({ theme }) => theme.colors.brand[500]};
  color: #fff;
  border: none;
  border-radius: ${({ theme }) => theme.radius.md};
  font-size: ${({ theme }) => theme.typography.fontSizes.base};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  transition:
    background 0.18s,
    opacity 0.18s;
  box-shadow: ${({ theme }) => theme.shadows.brand};

  &:hover:not(:disabled) {
    background: ${({ theme }) => theme.colors.brand[600]};
  }
  &:disabled {
    opacity: 0.5;
    box-shadow: none;
  }
`;

const WeightBanner = styled.div`
  display: flex;
  align-items: flex-start;
  gap: ${({ theme }) => theme.spacing[3]};
  background: ${({ theme }) => theme.colors.feedback.errorBg};
  border: 1px solid ${({ theme }) => theme.colors.feedback.error};
  color: ${({ theme }) => theme.colors.feedback.error};
  border-radius: ${({ theme }) => theme.radius.md};
  padding: ${({ theme }) => theme.spacing[4]};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  margin-bottom: ${({ theme }) => theme.spacing[5]};
`;

const ErrorBanner = styled.div`
  background: ${({ theme }) => theme.colors.feedback.errorBg};
  border: 1px solid ${({ theme }) => theme.colors.feedback.error};
  color: ${({ theme }) => theme.colors.feedback.error};
  border-radius: ${({ theme }) => theme.radius.md};
  padding: ${({ theme }) => theme.spacing[3]} ${({ theme }) => theme.spacing[4]};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  margin-bottom: ${({ theme }) => theme.spacing[5]};
`;

const ResultSection = styled.div<{
  "aria-live"?: string;
  "aria-busy"?: string | boolean;
  "aria-label"?: string;
}>`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing[5]};
`;

const TabBar = styled.div`
  display: flex;
  gap: ${({ theme }) => theme.spacing[2]};
  flex-wrap: wrap;
`;

const Tab = styled.button<{ $active: boolean; $color?: string }>`
  padding: 7px 18px;
  border-radius: ${({ theme }) => theme.radius.full};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  font-weight: ${({ theme, $active }) =>
    $active
      ? theme.typography.fontWeights.bold
      : theme.typography.fontWeights.medium};
  border: 1px solid
    ${({ theme, $color, $active }) =>
      $active ? ($color ?? theme.colors.brand[500]) : theme.colors.border};
  background: ${({ theme, $color, $active }) =>
    $active ? ($color ?? theme.colors.brand[500]) : theme.colors.surface};
  color: ${({ $active }) => ($active ? "#fff" : undefined)};
  transition:
    background 0.18s,
    border-color 0.18s,
    color 0.18s;

  &:hover:not([aria-selected="true"]) {
    border-color: ${({ theme, $color }) => $color ?? theme.colors.brand[500]};
    color: ${({ theme, $color }) => $color ?? theme.colors.brand[500]};
  }
`;

const CardsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: ${({ theme }) => theme.spacing[4]};
  ${media.md} {
    grid-template-columns: repeat(3, 1fr);
  }
`;

const SkeletonCard = styled.div`
  background: ${({ theme }) => theme.colors.surface};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.lg};
  padding: ${({ theme }) => theme.spacing[5]};
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing[3]};
`;

const RouteCard = styled.article<{ $color: string; $selected: boolean }>`
  background: ${({ theme }) => theme.colors.surface};
  border: 2px solid
    ${({ theme, $color, $selected }) =>
      $selected ? $color : theme.colors.border};
  border-top: 4px solid ${({ $color }) => $color};
  border-radius: ${({ theme }) => theme.radius.lg};
  padding: ${({ theme }) => theme.spacing[5]};
  cursor: pointer;
  transition:
    border-color 0.2s,
    box-shadow 0.2s,
    transform 0.2s;
  box-shadow: ${({ theme, $color, $selected }) =>
    $selected ? `0 4px 16px ${$color}40` : theme.shadows.sm};

  &:hover {
    transform: translateY(-2px);
    border-color: ${({ $color }) => $color};
  }
  &:focus-visible {
    outline: 2px solid ${({ $color }) => $color};
    outline-offset: 2px;
  }
`;

const CardHeader = styled.div`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[2]};
  margin-bottom: ${({ theme }) => theme.spacing[3]};
`;

const CardIcon = styled.div<{ $color: string }>`
  width: 32px;
  height: 32px;
  border-radius: ${({ theme }) => theme.radius.md};
  background: ${({ $color }) => $color};
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
`;

const CardTitle = styled.h3`
  font-size: ${({ theme }) => theme.typography.fontSizes.base};
  font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
  flex: 1;
`;

const SelectedIndicator = styled.span`
  color: ${({ theme }) => theme.colors.textMuted};
`;

const BadgeRow = styled.div`
  display: flex;
  gap: ${({ theme }) => theme.spacing[1]};
  margin-bottom: ${({ theme }) => theme.spacing[3]};
  flex-wrap: wrap;
`;

const Badge = styled.span<{ $color: string }>`
  display: inline-block;
  padding: 3px 9px;
  border-radius: ${({ theme }) => theme.radius.full};
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
  background: ${({ $color }) => $color + "1a"};
  color: ${({ $color }) => $color};
  letter-spacing: 0.02em;
`;

const MetricList = styled.div`
  display: flex;
  flex-direction: column;
`;

const MetricRow = styled.div<{ $last?: boolean }>`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: ${({ theme }) => theme.spacing[2]} 0;
  border-bottom: ${({ theme, $last }) =>
    $last ? "none" : `1px dashed ${theme.colors.border}`};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
`;

const MetricLabel = styled.span`
  color: ${({ theme }) => theme.colors.textMuted};
`;

const MetricValue = styled.span`
  font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
  color: ${({ theme }) => theme.colors.text};
`;

const StopSequence = styled.div`
  background: ${({ theme }) => theme.colors.surface};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.lg};
  padding: ${({ theme }) => theme.spacing[5]};
  box-shadow: ${({ theme }) => theme.shadows.sm};
`;

const StopTitle = styled.h3`
  font-size: ${({ theme }) => theme.typography.fontSizes.base};
  font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
  margin-bottom: ${({ theme }) => theme.spacing[4]};
`;

const StopList = styled.ol`
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing[2]};
`;

const StopItem = styled.li`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[3]};
  padding: ${({ theme }) => theme.spacing[2]} 0;
  border-bottom: 1px dashed ${({ theme }) => theme.colors.border};
  &:last-child {
    border-bottom: none;
  }
`;

const StopNum = styled.span`
  width: 24px;
  height: 24px;
  border-radius: ${({ theme }) => theme.radius.full};
  background: ${({ theme }) => theme.colors.brand[500]};
  color: #fff;
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
`;

const StopLabel = styled.p`
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
`;

const StopCoords = styled.p`
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  color: ${({ theme }) => theme.colors.textMuted};
`;
