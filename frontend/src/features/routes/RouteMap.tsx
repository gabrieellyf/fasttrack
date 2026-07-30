import {
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  ReferenceDot,
  ResponsiveContainer,
  Scatter,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import styled, { useTheme } from "styled-components";
import { useTranslation } from "react-i18next";
import type { RouteOption } from "../../types";

interface StopPoint {
  x: number;
  y: number;
  label: string;
}

function routeToLineData(route: RouteOption): StopPoint[] {
  return route.stops.map((s) => ({ x: s.x, y: s.y, label: s.label }));
}

interface RouteMapProps {
  express: RouteOption;
  economic: RouteOption;
  strategic: RouteOption;
  activeRoute?: "express" | "economic" | "strategic";
}

export function RouteMap({
  express,
  economic,
  strategic,
  activeRoute,
}: RouteMapProps) {
  const { t } = useTranslation();
  const theme = useTheme();

  const colors = {
    express: theme.colors.strategies.express,
    economic: theme.colors.strategies.economic,
    strategic: theme.colors.strategies.strategic,
  };

  const labels = {
    express: t("routing.strategies.express"),
    economic: t("routing.strategies.economic"),
    strategic: t("routing.strategies.strategic"),
  };

  const expressData = routeToLineData(express);
  const economicData = routeToLineData(economic);
  const strategicData = routeToLineData(strategic);

  const isVisible = (type: string) =>
    activeRoute == null || activeRoute === type;

  const deliveryStops = express.stops
    .filter((s) => !s.label.toLowerCase().includes("hub"))
    .filter((s, i, arr) => arr.findIndex((x) => x.id === s.id) === i)
    .map((s) => ({ x: s.x, y: s.y, name: s.label }));

  const hubStop = express.stops.find((s) =>
    s.label.toLowerCase().includes("hub"),
  );

  const allRoutes = [
    { type: "express" as const, data: express },
    { type: "economic" as const, data: economic },
    { type: "strategic" as const, data: strategic },
  ];

  return (
    <Wrapper>
      <ResponsiveContainer width="100%" height={380}>
        <ComposedChart margin={{ top: 20, right: 20, bottom: 24, left: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke={theme.colors.border} />
          <XAxis
            dataKey="x"
            type="number"
            name={t("routing.chart.xAxis")}
            label={{
              value: t("routing.chart.xAxis"),
              position: "insideBottom",
              offset: -12,
              fill: theme.colors.textMuted,
              fontSize: 12,
            }}
            tick={{ fill: theme.colors.textMuted, fontSize: 11 }}
            axisLine={{ stroke: theme.colors.border }}
            tickLine={{ stroke: theme.colors.border }}
          />
          <YAxis
            dataKey="y"
            type="number"
            name={t("routing.chart.yAxis")}
            label={{
              value: t("routing.chart.yAxis"),
              angle: -90,
              position: "insideLeft",
              fill: theme.colors.textMuted,
              fontSize: 12,
            }}
            tick={{ fill: theme.colors.textMuted, fontSize: 11 }}
            axisLine={{ stroke: theme.colors.border }}
            tickLine={{ stroke: theme.colors.border }}
          />
          <Tooltip
            content={({ payload }) => {
              if (!payload?.length) return null;
              const p = payload[0].payload as StopPoint;
              return (
                <TooltipBox>
                  <strong>{p.label ?? t("routing.chart.stops")}</strong>
                  <span>
                    ({p.x}, {p.y})
                  </span>
                </TooltipBox>
              );
            }}
          />
          <Legend
            wrapperStyle={{ fontSize: 12, color: theme.colors.textMuted }}
          />

          <Scatter
            name={t("routing.chart.stops")}
            data={deliveryStops}
            fill={theme.colors.textMuted}
            opacity={0.5}
          />

          {hubStop && (
            <ReferenceDot
              x={hubStop.x}
              y={hubStop.y}
              r={8}
              fill={theme.colors.brand[500]}
              stroke="#fff"
              strokeWidth={2}
            />
          )}

          {isVisible("express") && (
            <Line
              name={labels.express}
              data={expressData}
              dataKey="y"
              stroke={colors.express}
              strokeWidth={2.5}
              dot={{ r: 4, fill: colors.express, strokeWidth: 0 }}
              legendType="line"
              isAnimationActive={false}
            />
          )}
          {isVisible("economic") && (
            <Line
              name={labels.economic}
              data={economicData}
              dataKey="y"
              stroke={colors.economic}
              strokeWidth={2.5}
              dot={{ r: 4, fill: colors.economic, strokeWidth: 0 }}
              strokeDasharray="6 3"
              legendType="line"
              isAnimationActive={false}
            />
          )}
          {isVisible("strategic") && (
            <Line
              name={labels.strategic}
              data={strategicData}
              dataKey="y"
              stroke={colors.strategic}
              strokeWidth={2.5}
              dot={{ r: 4, fill: colors.strategic, strokeWidth: 0 }}
              strokeDasharray="3 3"
              legendType="line"
              isAnimationActive={false}
            />
          )}
        </ComposedChart>
      </ResponsiveContainer>

      {}
      <SummaryTable>
        <thead>
          <tr>
            <Th>Estratégia</Th>
            <Th>{t("routing.metrics.totalDistance")}</Th>
            <Th>{t("routing.metrics.totalCost")}</Th>
            <Th>{t("routing.metrics.totalWeight")}</Th>
          </tr>
        </thead>
        <tbody>
          {allRoutes.map(({ type, data }) => (
            <SummaryRow
              key={type}
              $active={activeRoute === type}
              $color={colors[type]}
            >
              <Td style={{ color: colors[type], fontWeight: 600 }}>
                {labels[type]}
              </Td>
              <Td>
                {data.total_distance.toFixed(2)}{" "}
                {t("routing.metrics.distanceUnit")}
              </Td>
              <Td>{data.total_cost.toFixed(2)}</Td>
              <Td>
                {data.total_weight.toFixed(1)} {t("routing.metrics.weightUnit")}
              </Td>
            </SummaryRow>
          ))}
        </tbody>
      </SummaryTable>
    </Wrapper>
  );
}

const Wrapper = styled.div`
  background: ${({ theme }) => theme.colors.surface};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.lg};
  box-shadow: ${({ theme }) => theme.shadows.md};
  overflow: hidden;
`;

const TooltipBox = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2px;
  background: ${({ theme }) => theme.colors.surface};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.md};
  padding: 8px 12px;
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  box-shadow: ${({ theme }) => theme.shadows.md};
`;

const SummaryTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  border-top: 1px solid ${({ theme }) => theme.colors.border};
`;

const Th = styled.th`
  padding: ${({ theme }) => theme.spacing[3]} ${({ theme }) => theme.spacing[4]};
  text-align: left;
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  color: ${({ theme }) => theme.colors.textMuted};
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
  background: ${({ theme }) => theme.colors.surface2};
`;

const SummaryRow = styled.tr<{ $active: boolean; $color: string }>`
  background: ${({ theme, $active }) =>
    $active ? theme.colors.brand[50] : "transparent"};
  font-weight: ${({ $active }) => ($active ? 600 : 400)};
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
  transition: background 0.18s;
  &:last-child {
    border-bottom: none;
  }
  &:hover {
    background: ${({ theme }) => theme.colors.surface2};
  }
`;

const Td = styled.td`
  padding: ${({ theme }) => theme.spacing[3]} ${({ theme }) => theme.spacing[4]};
  color: ${({ theme }) => theme.colors.text};
`;
