import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import styled from "styled-components";
import { Warehouse } from "lucide-react";
import { useTranslation } from "react-i18next";
import type { AppDispatch, RootState } from "../../store";
import { fetchHubs } from "../../store/slices/hubsSlice";
import { PageHeader } from "../../components/ui/PageHeader";
import { SkeletonTable } from "../../components/ui/Skeleton";
import { EmptyState } from "../../components/ui/EmptyState";

export function HubList() {
  const dispatch = useDispatch<AppDispatch>();
  const { t } = useTranslation();
  const { items, loading, error } = useSelector((s: RootState) => s.hubs);

  useEffect(() => {
    dispatch(fetchHubs());
  }, [dispatch]);

  const cols = [
    t("hubs.columns.name"),
    t("hubs.columns.x"),
    t("hubs.columns.y"),
    t("hubs.columns.type"),
  ];

  return (
    <Container>
      <PageHeader title={t("hubs.title")} />

      {error && (
        <ErrorBanner role="alert">
          {t("common.error", { message: error })}
        </ErrorBanner>
      )}

      {loading && !items.length && <SkeletonTable rows={4} cols={4} />}

      {!loading && !error && items.length === 0 && (
        <EmptyState icon={<Warehouse size={28} />} title={t("hubs.empty")} />
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
              {items.map((hub, idx) => (
                <Tr key={hub.id} $even={idx % 2 === 0}>
                  <Td data-label={cols[0]}>{hub.name}</Td>
                  <Td data-label={cols[1]}>{hub.x}</Td>
                  <Td data-label={cols[2]}>{hub.y}</Td>
                  <Td data-label={cols[3]}>
                    <TypeBadge $central={hub.is_central}>
                      {hub.is_central
                        ? t("hubs.types.central")
                        : t("hubs.types.secondary")}
                    </TypeBadge>
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
  max-width: 800px;
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

const TypeBadge = styled.span<{ $central: boolean }>`
  display: inline-block;
  padding: 3px 10px;
  border-radius: ${({ theme }) => theme.radius.full};
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
  background: ${({ theme, $central }) =>
    $central ? theme.colors.brand[50] : "rgba(139,92,246,0.1)"};
  color: ${({ theme, $central }) =>
    $central ? theme.colors.brand[700] : "#6d28d9"};
  letter-spacing: 0.02em;
`;
