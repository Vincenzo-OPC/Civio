import { useId } from 'react';
import type { ReactNode } from 'react';
import type { AskAssistant } from '@/lib/ai-handoff';

function Mark({
    className,
    children,
}: {
    className: string;
    children: ReactNode;
}) {
    return (
        <svg
            viewBox="0 0 24 24"
            className={`${className} shrink-0`}
            aria-hidden
        >
            {children}
        </svg>
    );
}

/** The ChatGPT knot, the same mark Chrome puts beside Ask ChatGPT. */
export function ChatGptMark({ className = 'size-4' }: { className?: string }) {
    return (
        <Mark className={className}>
            <path
                fill="currentColor"
                d="M22.282 9.821a5.985 5.985 0 0 0-.516-4.91 6.046 6.046 0 0 0-6.51-2.9A6.065 6.065 0 0 0 4.981 4.18a5.985 5.985 0 0 0-3.998 2.9 6.046 6.046 0 0 0 .743 7.097 5.98 5.98 0 0 0 .51 4.911 6.051 6.051 0 0 0 6.515 2.9A5.985 5.985 0 0 0 13.26 24a6.056 6.056 0 0 0 5.772-4.206 5.99 5.99 0 0 0 3.997-2.9 6.056 6.056 0 0 0-.747-7.073zM13.26 22.43a4.476 4.476 0 0 1-2.876-1.04l.141-.081 4.779-2.758a.795.795 0 0 0 .392-.681v-6.737l2.02 1.168a.071.071 0 0 1 .038.052v5.583a4.504 4.504 0 0 1-4.494 4.494zM3.6 18.304a4.47 4.47 0 0 1-.535-3.014l.142.085 4.783 2.759a.771.771 0 0 0 .78 0l5.843-3.369v2.332a.08.08 0 0 1-.033.062L9.74 19.95a4.5 4.5 0 0 1-6.14-1.646zM2.34 7.896a4.485 4.485 0 0 1 2.366-1.973V11.6a.766.766 0 0 0 .387.676l5.815 3.355-2.02 1.168a.076.076 0 0 1-.071 0l-4.83-2.786A4.504 4.504 0 0 1 2.34 7.872zm16.597 3.855-5.833-3.387 2.02-1.164a.08.08 0 0 1 .071 0l4.83 2.791a4.494 4.494 0 0 1-.676 8.105v-5.678a.79.79 0 0 0-.412-.667zm2.01-3.023-.141-.085-4.774-2.782a.776.776 0 0 0-.785 0L9.409 9.23V6.897a.066.066 0 0 1 .028-.061l4.83-2.787a4.5 4.5 0 0 1 6.68 4.66zM8.306 12.863l-2.02-1.164a.08.08 0 0 1-.038-.057V6.075a4.5 4.5 0 0 1 7.375-3.453l-.142.08-4.778 2.758a.795.795 0 0 0-.393.681zm1.097-2.365 2.602-1.5 2.607 1.5v2.999l-2.597 1.5-2.607-1.5z"
            />
        </Mark>
    );
}

/** Gemini's four-point spark. */
export function GeminiMark({ className = 'size-4' }: { className?: string }) {
    const id = useId();

    return (
        <Mark className={className}>
            <defs>
                <linearGradient
                    id={id}
                    x1="0"
                    y1="24"
                    x2="24"
                    y2="0"
                    gradientUnits="userSpaceOnUse"
                >
                    <stop stopColor="#4B90FF" />
                    <stop offset="0.5" stopColor="#9B6DFF" />
                    <stop offset="1" stopColor="#F0718A" />
                </linearGradient>
            </defs>
            <path
                fill={`url(#${id})`}
                d="M11.04 19.32Q12 21.51 12 24q0-2.49.93-4.68.96-2.19 2.58-3.81t3.81-2.55Q21.51 12 24 12q-2.49 0-4.68-.93a12.3 12.3 0 0 1-3.81-2.58 12.3 12.3 0 0 1-2.58-3.81Q12 2.49 12 0q0 2.49-.96 4.68-.93 2.19-2.55 3.81a12.3 12.3 0 0 1-3.81 2.58Q2.49 12 0 12q2.49 0 4.68.96 2.19.93 3.81 2.55t2.55 3.81"
            />
        </Mark>
    );
}

/** Copilot's ribbon. */
export function CopilotMark({ className = 'size-4' }: { className?: string }) {
    const id = useId();

    return (
        <Mark className={className}>
            <defs>
                <linearGradient
                    id={id}
                    x1="2"
                    y1="22"
                    x2="22"
                    y2="2"
                    gradientUnits="userSpaceOnUse"
                >
                    <stop stopColor="#2B7FFF" />
                    <stop offset="0.55" stopColor="#8A5CFF" />
                    <stop offset="1" stopColor="#F2638A" />
                </linearGradient>
            </defs>
            <path
                fill={`url(#${id})`}
                d="M9 23l.073-.001a2.53 2.53 0 01-2.347-1.838l-.697-2.433a2.529 2.529 0 00-2.426-1.839h-.497l-.104-.002c-4.485 0-2.935-5.278-1.75-9.225l.162-.525C2.412 3.99 3.883 1 6.25 1h8.86c1.12 0 2.106.745 2.422 1.829l.715 2.453a2.53 2.53 0 002.247 1.823l.147.005.534.001c3.557.115 3.088 3.745 2.156 7.206l-.113.413c-.154.548-.315 1.089-.47 1.607l-.163.525C21.588 20.01 20.116 23 17.75 23h-8.75zm8.22-15.89l-3.856.001a2.526 2.526 0 00-2.35 1.615L9.21 15.04a2.529 2.529 0 01-2.43 1.847l3.853.002c1.056 0 1.992-.661 2.361-1.644l1.796-6.287a2.529 2.529 0 012.43-1.848z"
            />
        </Mark>
    );
}

/** Grok's mark. It is black on paper and white in dark mode. */
export function GrokMark({ className = 'size-4' }: { className?: string }) {
    return (
        <Mark className={className}>
            <path
                fill="currentColor"
                d="M9.27 15.29l7.978-5.897c.391-.29.95-.177 1.137.272.98 2.369.542 5.215-1.41 7.169-1.951 1.954-4.667 2.382-7.149 1.406l-2.711 1.257c3.889 2.661 8.611 2.003 11.562-.953 2.341-2.344 3.066-5.539 2.388-8.42l.006.007c-.983-4.232.242-5.924 2.75-9.383.06-.082.12-.164.179-.248l-3.301 3.305v-.01L9.267 15.292M7.623 16.723c-2.792-2.67-2.31-6.801.071-9.184 1.761-1.763 4.647-2.483 7.166-1.425l2.705-1.25a7.808 7.808 0 00-1.829-1A8.975 8.975 0 005.984 5.83c-2.533 2.536-3.33 6.436-1.962 9.764 1.022 2.487-.653 4.246-2.34 6.022-.599.63-1.199 1.259-1.682 1.925l7.62-6.815"
            />
        </Mark>
    );
}

/** No brand. Used when the preference is just Ask AI. */
export function AskAiMark({ className = 'size-4' }: { className?: string }) {
    return (
        <Mark className={className}>
            <path
                fill="currentColor"
                d="M12 1.8 13.15 8.9 20.2 10.1 13.15 11.3 12 18.4 10.85 11.3 3.8 10.1 10.85 8.9z"
            />
        </Mark>
    );
}

export function AssistantMark({
    assistant,
    className,
}: {
    assistant: AskAssistant;
    className?: string;
}) {
    if (assistant === 'gemini') {
        return <GeminiMark className={className} />;
    }

    if (assistant === 'copilot') {
        return <CopilotMark className={className} />;
    }

    if (assistant === 'grok') {
        return <GrokMark className={className} />;
    }

    if (assistant === 'ai') {
        return <AskAiMark className={className} />;
    }

    return <ChatGptMark className={className} />;
}
