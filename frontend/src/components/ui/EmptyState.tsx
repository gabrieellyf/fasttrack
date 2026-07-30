import type { ReactNode } from "react";
import styled from "styled-components";

interface EmptyStateProps {
  icon: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
}

export function EmptyState({
  icon,
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <Container role="status">
      <IconWrap aria-hidden="true">{icon}</IconWrap>
      <Title>{title}</Title>
      {description && <Desc>{description}</Desc>}
      {action && <ActionSlot>{action}</ActionSlot>}
    </Container>
  );
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: ${({ theme }) => theme.spacing[16]}
    ${({ theme }) => theme.spacing[6]};
  text-align: center;
  gap: ${({ theme }) => theme.spacing[3]};
`;

const IconWrap = styled.div`
  width: 56px;
  height: 56px;
  border-radius: ${({ theme }) => theme.radius.lg};
  background: ${({ theme }) => theme.colors.surface2};
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${({ theme }) => theme.colors.textMuted};
  margin-bottom: ${({ theme }) => theme.spacing[2]};
`;

const Title = styled.p`
  font-size: ${({ theme }) => theme.typography.fontSizes.base};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  color: ${({ theme }) => theme.colors.text};
`;

const Desc = styled.p`
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textMuted};
  max-width: 320px;
`;

const ActionSlot = styled.div`
  margin-top: ${({ theme }) => theme.spacing[2]};
`;
