export interface AiModelOption {
    value: string;
    label: string;
    provider: 'gemini' | 'cloudflare';
    badge?: string;
}

export const AI_MODEL_OPTIONS: AiModelOption[] = [
    // Google Gemini Models
    {
        value: 'gemini-3.7-flash',
        label: 'Google Gemini 3.7 Flash (Recommended — Best for CSE & SVGs)',
        provider: 'gemini',
        badge: 'Recommended',
    },
    {
        value: 'gemini-3.7-pro',
        label: 'Google Gemini 3.7 Pro (Advanced Reasoning & Multi-step Problems)',
        provider: 'gemini',
    },
    {
        value: 'gemini-3.6-flash',
        label: 'Google Gemini 3.6 Flash (Stable High Performance)',
        provider: 'gemini',
    },
    {
        value: 'gemini-3.5-flash',
        label: 'Google Gemini 3.5 Flash (Standard Fast)',
        provider: 'gemini',
    },
    {
        value: 'gemini-2.5-flash',
        label: 'Google Gemini 2.5 Flash',
        provider: 'gemini',
    },
    {
        value: 'gemini-1.5-pro',
        label: 'Google Gemini 1.5 Pro (High Reasoning)',
        provider: 'gemini',
    },
    {
        value: 'gemini-1.5-flash',
        label: 'Google Gemini 1.5 Flash (Fast)',
        provider: 'gemini',
    },
    {
        value: 'gemini-1.5-flash-8b',
        label: 'Google Gemini 1.5 Flash-8B',
        provider: 'gemini',
    },

    // Cloudflare Workers AI Models
    {
        value: '@cf/meta/llama-3.2-3b-instruct',
        label: 'Cloudflare Workers AI — Llama 3.2 3B Instruct',
        provider: 'cloudflare',
        badge: 'CF Default',
    },
    {
        value: '@cf/meta/llama-3.2-1b-instruct',
        label: 'Cloudflare Workers AI — Llama 3.2 1B Instruct (Ultra Fast)',
        provider: 'cloudflare',
        badge: 'Fast',
    },
    {
        value: '@cf/meta/llama-3.3-70b-instruct',
        label: 'Cloudflare Workers AI — Llama 3.3 70B Instruct (High Capability)',
        provider: 'cloudflare',
    },
    {
        value: '@cf/deepseek-ai/deepseek-r1-distill-qwen-32b',
        label: 'Cloudflare Workers AI — DeepSeek R1 Distill Qwen 32B (Reasoning)',
        provider: 'cloudflare',
    },
];

export const DEFAULT_ADMIN_AI_MODEL = 'gemini-3.7-flash';
export const DEFAULT_WORKERS_AI_MODEL = '@cf/meta/llama-3.2-3b-instruct';
