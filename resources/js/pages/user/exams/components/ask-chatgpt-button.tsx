import { toast } from 'sonner';
import {
    buildAiHandoffText,
    chatgptAskUrl,
    writeClipboardText,
} from '@/lib/ai-handoff';
import type {
    AiHandoffAttemptState,
    AiHandoffOptions,
    AiHandoffQuestion,
} from '@/lib/ai-handoff';

interface AskChatGptButtonProps {
    question: AiHandoffQuestion;
    attempt: AiHandoffAttemptState;
    options?: AiHandoffOptions;
    className?: string;
}

/**
 * Opens ChatGPT with this question, the same job as Chrome's right-click
 * "Ask ChatGPT". The link is the handoff text. The clipboard copy is only
 * the fallback when the question is too long for the address.
 */
export function AskChatGptButton({
    question,
    attempt,
    options,
    className,
}: AskChatGptButtonProps) {
    const text = buildAiHandoffText(question, attempt, options);
    const href = chatgptAskUrl(text);
    const prefilled = href.includes('?q=');

    return (
        <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            title="Open this question in ChatGPT"
            onClick={() => {
                void writeClipboardText(text).then((ok) => {
                    if (prefilled) {
                        toast.success('Opened in ChatGPT.', {
                            id: 'ask-chatgpt',
                        });

                        return;
                    }

                    toast[ok ? 'success' : 'error'](
                        ok
                            ? 'Copied. Paste it into ChatGPT.'
                            : 'Could not copy. Your browser blocked the clipboard.',
                        { id: 'ask-chatgpt' },
                    );
                });
            }}
            className={
                className ??
                'inline-flex cursor-pointer items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-[11px] font-bold text-muted-foreground no-underline transition hover:bg-muted focus:outline-none'
            }
        >
            Ask ChatGPT
        </a>
    );
}
