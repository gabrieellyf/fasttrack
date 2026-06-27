import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import styled from "styled-components";
import { Truck } from "lucide-react";
import { useTranslation } from "react-i18next";
import type { AppDispatch, RootState } from "../../store";
import { fetchVehicles } from "../../store/slices/vehiclesSlice";
import { PageHeader } from "../../components/ui/PageHeader";
import { SkeletonTable } from "../../components/ui/Skeleton";
import { EmptyState } from "../../components/ui/EmptyState";

export function VehicleList() {
  const dispatch = useDispatch<AppDispatch>();
  const { t } = useTranslation();
  const { items, loading, error } = useSelector((s: RootState) => s.vehicles);

  useEffect(() => {
    dispatch(fetchVehicles());
  }, [dispatch]);

  const cols = [
    t("vehicles.columns.plate"),
    t("vehicles.columns.maxWeight"),
    t("vehicles.columns.createdAt"),
  ];

  return (
    <Container>
      <PageHeader title={t("vehicles.title")} />

      {error && (
        <ErrorBanner role="alert">
          {t("common.error", { message: error })}
        </ErrorBanner>
      )}

      {loading && !items.length && <SkeletonTable rows={4} cols={3} />}

      {!loading && !error && items.length === 0 && (
        <EmptyState icon={<Truck size={28} />} title={t("vehicles.empty")} />
      )}

      {items.length > 0 && (
        <TableWrapper>
          <Table>
            <thead>
              <tr>
                {cols.map((c) => (
                  <Th key={c}>{c}</Th>
                ))}
              </tr>
            </thead>
            <tbody>
              {items.map((v, idx) => (
                <Tr key={v.id} $even={idx % 2 === 0}>
                  <Td data-label={cols[0]}>
                    <PlateChip>{v.plate}</PlateChip>
                  </Td>
                  <Td data-label={cols[1]}>{v.max_weight} kg</Td>
                  <Td data-label={cols[2]}>
                    {new Date(v.created_at).toLocaleDateString("pt-BR")}
                  </Td>
                </Tr>
              ))}
            </tbody>
          </Table>
        </TableWrapper>
      )}
    </Container>
  );
}

const Container = styled.div`
  max-width: 720px;
`;

const ErrorBanner = styled.div`
  background: ${({ theme }) => theme.colors.feedback.errorBg};
  border: 1px solid ${({ theme }) => theme.colors.feedback.error};
  color: ${({ theme }) => theme.colors.feedback.error};
  border-radius: ${({ theme }) => theme.radius.md};
  padding: ${({ theme }) => theme.spacing[3]} ${({ theme }) => theme.spacing[4]};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  margin-bottom: ${({ theme }) => theme.spacing[4]};
`;

const TableWrapper = styled.div`
  background: ${({ theme }) => theme.colors.surface};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.lg};
  box-shadow: ${({ theme }) => theme.shadows.md};
  overflow: hidden;
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};

  @media (max-width: 767px) {
    display: block;
    thead {
      display: none;
    }
    tbody {
      display: block;
    }
  }
`;

const Th = styled.th`
  padding: ${({ theme }) => theme.spacing[3]} ${({ theme }) => theme.spacing[4]};
  text-align: left;
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  color: ${({ theme }) => theme.colors.textMuted};
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 2px solid ${({ theme }) => theme.colors.border};
  white-space: nowrap;
`;

const Tr = styled.tr<{ $even: boolean }>`
  background: ${({ theme, $even }) =>
    $even ? theme.colors.surface : theme.colors.surface2 + "60"};
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
  transition: background 0.15s;
  &:last-child {
    border-bottom: none;
  }
  &:hover {
    background: ${({ theme }) => theme.colors.brand[50]};
  }

  @media (max-width: 767px) {
    display: block;
    margin: ${({ theme }) => theme.spacing[3]};
    border-radius: ${({ theme }) => theme.radius.md};
    border: 1px solid ${({ theme }) => theme.colors.border};
    box-shadow: ${({ theme }) => theme.shadows.sm};
    &:last-child {
      border-bottom: 1px solid ${({ theme }) => theme.colors.border};
    }
  }
`;

const Td = styled.td`
  padding: ${({ theme }) => theme.spacing[3]} ${({ theme }) => theme.spacing[4]};
  color: ${({ theme }) => theme.colors.text};
  vertical-align: middle;

  @media (max-width: 767px) {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: ${({ theme }) => theme.spacing[2]}
      ${({ theme }) => theme.spacing[3]};
    border-bottom: 1px dashed ${({ theme }) => theme.colors.border};
    &:last-child {
      border-bottom: none;
    }
    &::before {
      content: attr(data-label);
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      color: ${({ theme }) => theme.colors.textMuted};
      font-size: ${({ theme }) => theme.typography.fontSizes.xs};
      margin-right: ${({ theme }) => theme.spacing[3]};
      flex-shrink: 0;
    }
  }
`;

const PlateChip = styled.span`
  display: inline-block;
  background: ${({ theme }) => theme.colors.brand[50]};
  color: ${({ theme }) => theme.colors.brand[700]};
  border: 1px solid ${({ theme }) => theme.colors.brand[100]};
  border-radius: ${({ theme }) => theme.radius.sm};
  padding: 2px 8px;
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
  font-family: monospace;
  letter-spacing: 0.05em;
`;
