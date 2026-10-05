import type React from 'react';
import { useRef } from 'react';

/**
 * Content shield disabled for Civio local/study use (copy-paste allowed).
 * Stub keeps the same hook API so exam views do not need a larger rewrite.
 */

interface UseContentShieldOptions {
    onCopyAttempt?: (msg: string) => void;
    onShieldActivate?: () => void;
    contentLabel?: 'Exam' | 'Review' | 'Drill' | 'Custom Drill' | string;
}

interface UseContentShieldReturn {
    isShielded: boolean;
    isResumeLocked: boolean;
    dismissShield: () => void;
    styleBlock: string;
    contentRef: React.RefObject<HTMLDivElement | null>;
    wrapperProps: {
        onCopy: (e: React.ClipboardEvent) => void;
        onContextMenu: (e: React.MouseEvent) => void;
        onMouseDown: (e: React.MouseEvent) => void;
        onDragStart: (e: React.DragEvent) => void;
    };
}

export function useContentShield(
    options: UseContentShieldOptions = {},
): UseContentShieldReturn {
    void options;
    const contentRef = useRef<HTMLDivElement | null>(null);

    return {
        isShielded: false,
        isResumeLocked: false,
        dismissShield: () => {},
        styleBlock: '',
        contentRef,
        wrapperProps: {
            onCopy: () => {},
            onContextMenu: () => {},
            onMouseDown: () => {},
            onDragStart: () => {},
        },
    };
}
