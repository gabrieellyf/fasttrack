import { useEffect, useRef } from "react";
import { createPortal } from "react-dom";
import styled from "styled-components";
import { AlertTriangle } from "lucide-react";

interface ConfirmDialogProps {
  isOpen: boolean;
  title: string;
  description?: string;
  confirmLabel?: string;
  cancelLabel?: string;
  variant?: "danger" | "default";
  onConfirm: () => void;
  onCancel: () => void;
}

export function ConfirmDialog({
  isOpen,
  title,
  description,
  confirmLabel = "Confirmar",
  cancelLabel = "Cancelar",
  variant = "default",
  onConfirm,
  onCancel,
}: ConfirmDialogProps) {
  const confirmRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    confirmRef.current?.focus();

    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onCancel();
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [isOpen, onCancel]);

  if (!isOpen) return null;

  return createPortal(
    <Overlay onClick={onCancel} role="presentation">
      <Dialog
        role="dialog"
        aria-modal="true"
        aria-labelledby="confirm-title"
        aria-describedby={description ? "confirm-desc" : undefined}
        onClick={(e) => e.stopPropagation()}
      >
        {variant === "danger" && (
          <IconWrap aria-hidden="true">
            <AlertTriangle size={22} />
          </IconWrap>
        )}
        <DialogTitle id="confirm-title">{title}</DialogTitle>
        {description && (
          <DialogDesc id="confirm-desc">{description}</DialogDesc>
        )}
        <Actions>
          <CancelBtn onClick={onCancel}>{cancelLabel}</CancelBtn>
          <ConfirmBtn
            ref={confirmRef}
            $danger={variant === "danger"}
            onClick={onConfirm}
          >
            {confirmLabel}
          </ConfirmBtn>
        </Actions>
      </Dialog>
    </Overlay>,
    document.body,
  );
}

const Overlay = styled.div`
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: ${({ theme }) => theme.zIndices.modal};
  padding: ${({ theme }) => theme.spacing[4]};
`;

const Dialog = styled.div`
  background: ${({ theme }) => theme.colors.surface};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.radius.xl};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.lg};
  max-width: 400px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing[3]};
`;

const IconWrap = styled.div`
  width: 44px;
  height: 44px;
  border-radius: ${({ theme }) => theme.radius.lg};
  background: ${({ theme }) => theme.colors.feedback.errorBg};
  color: ${({ theme }) => theme.colors.feedback.error};
  display: flex;
  align-items: center;
  justify-content: center;
`;

const DialogTitle = styled.h3`
  font-size: ${({ theme }) => theme.typography.fontSizes.lg};
  font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
  color: ${({ theme }) => theme.colors.text};
`;

const DialogDesc = styled.p`
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textMuted};
  line-height: ${({ theme }) => theme.typography.lineHeights.relaxed};
`;

const Actions = styled.div`
  display: flex;
  justify-content: flex-end;
  gap: ${({ theme }) => theme.spacing[2]};
  margin-top: ${({ theme }) => theme.spacing[2]};
`;

const baseBtn = `
  padding: 9px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: opacity 0.18s, background 0.18s;
  &:hover { opacity: 0.85; }
`;

const CancelBtn = styled.button`
  ${baseBtn}
  background: ${({ theme }) => theme.colors.surface2};
  color: ${({ theme }) => theme.colors.text};
  border: 1px solid ${({ theme }) => theme.colors.border};
`;

const ConfirmBtn = styled.button<{ $danger: boolean }>`
  ${baseBtn}
  background: ${({ theme, $danger }) =>
    $danger ? theme.colors.feedback.error : theme.colors.brand[500]};
  color: #fff;
`;
