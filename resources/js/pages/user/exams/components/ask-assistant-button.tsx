import { useSyncExternalStore } from 'react';
import { toast } from 'sonner';
import { AssistantMark } from '@/components/domain/assistant-mark';
import {
    assistantAskUrl,
    buildAiHandoffText,
    writeClipboardText,
} from '@/lib/ai-handoff';
import type {
    AiHandoffAttemptState,
    AiHandoffOptions,
    AiHandoffQuestion,
    AskAssistant,
} from '@/lib/ai-handoff';
import { readAskAssistant, subscribeAskAssistant } from '@/lib/ask-assistant';

interface AskAssistantButtonProps {
    question: AiHandoffQuestion;
    attempt: AiHandoffAttemptState;
    options?: AiHandoffOptions;
    className?: string;
}

const NAME: Record<AskAssistant, string> = {
    chatgpt: 'ChatGPT',
    gemini: 'Gemini',
};

/**
 * Opens the learner's chosen assistant with this question. The mark matches
 * the Chrome menu item. The clipboard copy is the fallback when the question
 * is too long for the address, or when the site does not fill the box.
 */
export function AskAssistantButton({
    question,
    attempt,
    options,
    className,
}: AskAssistantButtonProps) {
    const assistant = useSyncExternalStore(
        subscribeAskAssistant,
        readAskAssistant,
        () => 'chatgpt' as const,
    );
    const text = buildAiHandoffText(question, attempt, options);
    const href = assistantAskUrl(assistant, text);
    const prefilled = href.includes('?q=');
    const label = `Ask ${NAME[assistant]}`;

    return (
        <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            title={`Open this question in ${NAME[assistant]}`}
            onClick={() => {
                void writeClipboardText(text).then((ok) => {
                    if (prefilled) {
                        toast.success(`Opened in ${NAME[assistant]}.`, {
                            id: 'ask-assistant',
                        });

                        return;
                    }

                    toast[ok ? 'success' : 'error'](
                        ok
                            ? `Copied. Paste it into ${NAME[assistant]}.`
                            : 'Could not copy. Your browser blocked the clipboard.',
                        { id: 'ask-assistant' },
                    );
                });
            }}
            className={
                className ??
                'inline-flex cursor-pointer items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-[11px] font-bold text-muted-foreground no-underline transition hover:bg-muted focus:outline-none'
            }
        >
            {assistant === 'gemini' ? (
                <AssistantMark assistant="gemini" className="size-3.5" />
            ) : (
                <AssistantMark assistant="chatgpt" className="size-3.5" />
            )}
            {label}
        </a>
    );
}
