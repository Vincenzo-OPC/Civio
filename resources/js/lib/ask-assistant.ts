import type { AskAssistant } from '@/lib/ai-handoff';

export const ASK_ASSISTANT_KEY = 'civio_ask_assistant';
const CHANGE_EVENT = 'civio-ask-assistant';

export function parseAskAssistant(value: string | null): AskAssistant {
    return value === 'gemini' ? 'gemini' : 'chatgpt';
}

export function readAskAssistant(): AskAssistant {
    if (typeof localStorage === 'undefined') {
        return 'chatgpt';
    }

    try {
        return parseAskAssistant(localStorage.getItem(ASK_ASSISTANT_KEY));
    } catch {
        return 'chatgpt';
    }
}

export function writeAskAssistant(value: AskAssistant): void {
    localStorage.setItem(ASK_ASSISTANT_KEY, value);
    window.dispatchEvent(new Event(CHANGE_EVENT));
}

export function subscribeAskAssistant(onChange: () => void): () => void {
    window.addEventListener(CHANGE_EVENT, onChange);
    window.addEventListener('storage', onChange);

    return () => {
        window.removeEventListener(CHANGE_EVENT, onChange);
        window.removeEventListener('storage', onChange);
    };
}
