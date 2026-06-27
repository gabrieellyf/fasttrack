import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import styled from "styled-components";
import { Package, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { useTranslation } from "react-i18next";
import type { AppDispatch, RootState } from "../../store";
import { fetchPackages, removePackage } from "../../store/slices/packagesSlice";
import { PageHeader } from "../../components/ui/PageHeader";
import { SkeletonTable } from "../../components/ui/Skeleton";
import { EmptyState } from "../../components/ui/EmptyState";
import { ConfirmDialog } from "../../components/ui/ConfirmDialog";
import { media } from "../../styles/theme";

export function PackageList() {
  const dispatch = useDispatch<AppDispatch>();
  const { t } = useTranslation();
  const { items, loading, error } = useSelector((s: RootState) => s.packages);
  const [pendingRemoveId, setPendingRemoveId] = useState<string | null>(null);

  useEffect(() => {
    dispatch(fetchPackages());
  }, [dispatch]);

  async function handleConfirmRemove() {
    if (!pendingRemoveId) return;
    const id = pendingRemoveId;
    setPendingRemoveId(null);
    try {
      await dispatch(removePackage(id)).unwrap();
      toast.success(t("packages.toasts.removed"));
    } catch {
      toast.error(t("packages.toasts.removeError"));
    }
  }

  const cols = [
    t("packages.columns.recipient"),
    t("packages.columns.x"),
    t("packages.columns.y"),
    t("packages.columns.weight"),
    t("packages.columns.accessCost"),
    t("packages.columns.actions"),
  ];

  return (
    <Container>
      <PageHeader title={t("packages.title")} />

      {error && (
        <ErrorBanner role="alert">
          {t("common.error", { message: error })}
        </ErrorBanner>
      )}

      {loading && !items.length && <SkeletonTable rows={6} cols={6} />}

      {!loading && !error && items.length === 0 && (
        <EmptyState icon={<Package size={28} />} title={t("packages.empty")} />
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
              {items.map((pkg, idx) => (
                <Tr key={pkg.id} $even={idx % 2 === 0}>
                  <Td data-label={cols[0]}>{pkg.recipient_name}</Td>
                  <Td data-label={cols[1]}>{pkg.x}</Td>
                  <Td data-label={cols[2]}>{pkg.y}</Td>
                  <Td data-label={cols[3]}>{pkg.weight}</Td>
                  <Td data-label={cols[4]}>{pkg.access_cost}</Td>
                  <Td data-label={cols[5]}>
                    <RemoveBtn
                      onClick={() => setPendingRemoveId(pkg.id)}
                      aria-label={`${t("packages.actions.remove")} ${pkg.recipient_name}`}
                      title={t("packages.actions.remove")}
                    >
                      <Trash2 size={15} aria-hidden="true" />
                      <BtnLabel>{t("packages.actions.remove")}</BtnLabel>
                    </RemoveBtn>
                  </Td>
                </Tr>
              ))}
            </tbody>
          </Table>
        </TableWrapper>
      )}

      <ConfirmDialog
        isOpen={pendingRemoveId !== null}
        title={t("packages.actions.confirmRemove")}
        description={t("packages.actions.confirmRemoveDesc")}
        confirmLabel={t("packages.actions.confirm")}
        cancelLabel={t("packages.actions.cancel")}
        variant="danger"
        onConfirm={handleConfirmRemove}
        onCancel={() => setPendingRemoveId(null)}
      />
    </Container>
  );
}

const Container = styled.div`
  max-width: 960px;
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

const RemoveBtn = styled.button`
  display: inline-flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[1]};
  padding: 5px 10px;
  border-radius: ${({ theme }) => theme.radius.md};
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  color: ${({ theme }) => theme.colors.feedback.error};
  background: ${({ theme }) => theme.colors.feedback.errorBg};
  border: 1px solid transparent;
  transition: border-color 0.18s;
  &:hover {
    border-color: ${({ theme }) => theme.colors.feedback.error};
  }
`;

const BtnLabel = styled.span`
  ${media.md} {
    display: none;
  }
`;
