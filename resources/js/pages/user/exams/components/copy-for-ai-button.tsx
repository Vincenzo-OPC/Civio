import { ClipboardCopy } from 'lucide-react';
import { toast } from 'sonner';
import { copyAiHandoff } from '@/lib/ai-handoff';
import type {
    AiHandoffAttemptState,
    AiHandoffOptions,
    AiHandoffQuestion,
} from '@/lib/ai-handoff';

interface CopyForAiButtonProps {
    question: AiHandoffQuestion;
    attempt: AiHandoffAttemptState;
    options?: AiHandoffOptions;
    className?: string;
}

/**
 * Copies a clean, structured version of the current question for any AI chat.
 * Never calls /exams/reveal: it only uses what the learner can already see.
 */
export function CopyForAiButton({
    question,
    attempt,
    options,
    className,
}: CopyForAiButtonProps) {
    const handleCopy = async () => {
        const { ok } = await copyAiHandoff(question, attempt, options);

        if (ok) {
            toast.success('Copied clean question for AI.', {
                id: 'copy-for-ai',
            });
        } else {
            toast.error('Could not copy. Your browser blocked the clipboard.', {
                id: 'copy-for-ai',
            });
        }
    };

    return (
        <button
            type="button"
            onClick={handleCopy}
            title="Copy this question as clean text for ChatGPT, Claude, Gemini or Grok"
            className={
                className ??
                'inline-flex cursor-pointer items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-[11px] font-bold text-muted-foreground transition hover:bg-muted focus:outline-none'
            }
        >
            <ClipboardCopy className="size-3.5" />
            <span>Copy for AI</span>
        </button>
    );
}
