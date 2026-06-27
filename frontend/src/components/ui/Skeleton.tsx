import styled, { keyframes } from "styled-components";

const shimmer = keyframes`
  0%   { background-position: -600px 0; }
  100% { background-position: 600px 0; }
`;

/** Animated shimmer block used for loading skeletons. */
export const SkeletonBox = styled.div<{
  $width?: string;
  $height?: string;
  $radius?: string;
}>`
  background: linear-gradient(
    90deg,
    ${({ theme }) => theme.colors.surface2} 25%,
    ${({ theme }) => theme.colors.border} 50%,
    ${({ theme }) => theme.colors.surface2} 75%
  );
  background-size: 1200px 100%;
  animation: ${shimmer} 1.6s ease-in-out infinite;
  border-radius: ${({ theme, $radius }) => $radius ?? theme.radius.md};
  width: ${({ $width }) => $width ?? "100%"};
  height: ${({ $height }) => $height ?? "16px"};
  flex-shrink: 0;
`;

const SkeletonRow = styled.div`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[3]};
  padding: ${({ theme }) => theme.spacing[3]} 0;
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
`;

interface SkeletonTableProps {
  rows?: number;
  cols?: number;
}

export function SkeletonTable({ rows = 5, cols = 4 }: SkeletonTableProps) {
  return (
    <div role="status" aria-label="Carregando dados..." aria-busy="true">
      {Array.from({ length: rows }).map((_, r) => (
        <SkeletonRow key={r}>
          {Array.from({ length: cols }).map((_, c) => (
            <SkeletonBox
              key={c}
              $height="14px"
              $width={c === 0 ? "35%" : c === cols - 1 ? "8%" : "15%"}
            />
          ))}
        </SkeletonRow>
      ))}
    </div>
  );
}
