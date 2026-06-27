import type { ReactNode } from "react";
import styled from "styled-components";

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  action?: ReactNode;
  id?: string;
}

export function PageHeader({ title, subtitle, action, id }: PageHeaderProps) {
  return (
    <Root>
      <TextGroup>
        <Title id={id}>{title}</Title>
        {subtitle && <Subtitle>{subtitle}</Subtitle>}
      </TextGroup>
      {action && <ActionSlot>{action}</ActionSlot>}
    </Root>
  );
}

const Root = styled.div`
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: ${({ theme }) => theme.spacing[4]};
  margin-bottom: ${({ theme }) => theme.spacing[6]};
  flex-wrap: wrap;
`;

const TextGroup = styled.div``;

const Title = styled.h1`
  font-size: ${({ theme }) => theme.typography.fontSizes["2xl"]};
  font-weight: ${({ theme }) => theme.typography.fontWeights.extrabold};
  color: ${({ theme }) => theme.colors.text};
  margin-bottom: ${({ theme }) => theme.spacing[1]};
`;

const Subtitle = styled.p`
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textMuted};
`;

const ActionSlot = styled.div`
  flex-shrink: 0;
`;
