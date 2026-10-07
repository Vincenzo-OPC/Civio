/**
 * Copy for AI: build a clean, provider-neutral plain-text handoff of the
 * current question for ChatGPT, Claude, Gemini, Grok or any chat box.
 *
 * Built only from structured question / attempt data — never from the DOM,
 * innerText, SVG or rendered HTML — so UI chrome (Report Issue, Flag,
 * Previous/Next, timers, icons) can never leak into the copied text.
 *
 * Answer safety: the correct answer, result and explanation are included only
 * when the attempt state explicitly says the answer was revealed or the
 * attempt is in review. Field presence alone (e.g. `question.correct_option`
 * already being in memory) never unlocks them.
 *
 * Spec: docs/EXTERNAL_AI_HANDOFF.md (MVP section).
 */

export type AiHandoffExamLevel =
    | 'Professional'
    | 'Subprofessional'
    | 'Practice';

export type AiHandoffMode = 'study' | 'live' | 'review';

export type AiHandoffResult = 'Correct' | 'Incorrect' | 'Not answered';

/** Structural subset of the exam `Question` type the formatter reads. */
export type AiHandoffQuestion = {
    stem: string;
    /** Options in the learner's current display (shuffled) order. */
    options: string[];
    category?: string | null;
    subcategory?: string | null;
    /** Verified source / rule for the item, when the bank has one. */
    source_rule?: string | null;
};

export type AiHandoffAttemptState = {
    /** Learner's choice as an index into the displayed options. */
    selectedDisplayIndex?: number | null;
    mode: AiHandoffMode;
    /** True only after the learner pressed Reveal for this question. */
    revealed: boolean;
    /** Verified correct option as an index into the displayed options. */
    verifiedCorrectDisplayIndex?: number | null;
    /** Civio's canonical explanation (from Reveal or the review payload). */
    verifiedExplanation?: string | null;
    result?: AiHandoffResult | null;
    learnerNote?: string | null;
    questionNumber: number;
    totalQuestions: number;
    examLevel: AiHandoffExamLevel;
};

export type AiHandoffOptions = {
    /** Include the learner's own note after Reveal / in review. Default false. */
    includeLearnerNote?: boolean;
};

export const AI_HANDOFF_HINT_PROMPT =
    'Do not reveal the correct answer yet. Give me one useful hint and help me reason it out.';

export const AI_HANDOFF_EXPLAIN_PROMPT =
    'Please explain this simply, tell me what to remember for the CSE, and give me one similar question.';

const NAMED_ENTITIES: Record<string, string> = {
    amp: '&',
    lt: '<',
    gt: '>',
    quot: '"',
    apos: "'",
    nbsp: ' ',
    ndash: '–',
    mdash: '—',
    hellip: '…',
    times: '×',
    divide: '÷',
    minus: '−',
    le: '≤',
    ge: '≥',
    ntilde: 'ñ',
    Ntilde: 'Ñ',
    lsquo: '‘',
    rsquo: '’',
    ldquo: '“',
    rdquo: '”',
    bull: '•',
    deg: '°',
    sup2: '²',
    sup3: '³',
    frac12: '½',
    radic: '√',
    peso: '₱',
};

const HTML_TAG =
    /<\/?(?:a|abbr|article|b|blockquote|br|center|code|del|div|em|font|h[1-6]|hr|i|ins|label|li|mark|ol|p|pre|s|section|small|span|strike|strong|sub|sup|table|tbody|td|th|thead|tr|u|ul)\b[^>]*>/gi;

const SUPERSCRIPT_DIGITS: Record<string, string> = {
    '0': '⁰',
    '1': '¹',
    '2': '²',
    '3': '³',
    '4': '⁴',
    '5': '⁵',
    '6': '⁶',
    '7': '⁷',
    '8': '⁸',
    '9': '⁹',
};

function superscript(inner: string): string {
    return /^\d+$/.test(inner)
        ? inner.replace(/\d/g, (d) => SUPERSCRIPT_DIGITS[d] ?? d)
        : `^(${inner})`;
}

function decodeEntities(text: string): string {
    return text.replace(
        /&(#x[0-9a-f]+|#\d+|[a-z][a-z0-9]*);/gi,
        (whole, body: string) => {
            if (body[0] === '#') {
                const code =
                    body[1] === 'x' || body[1] === 'X'
                        ? parseInt(body.slice(2), 16)
                        : parseInt(body.slice(1), 10);

                return Number.isFinite(code) && code > 0 && code <= 0x10ffff
                    ? String.fromCodePoint(code)
                    : whole;
            }

            return NAMED_ENTITIES[body] ?? whole;
        },
    );
}

/**
 * Plain-text version of bank text: drops HTML/SVG markup and light Markdown,
 * keeps line breaks and every Unicode character (ñ, —, ₱, ×, curly quotes…).
 */
export function toPlainText(input: string | null | undefined): string {
    if (!input) {
        return '';
    }

    let text = String(input).replace(/\r\n?/g, '\n');

    // Figures are SVG/images in the bank; their markup is not question text.
    text = text
        .replace(/<svg[\s\S]*?<\/svg>/gi, '[figure not included]')
        .replace(/<img\b[^>]*>/gi, '[figure not included]')
        .replace(/!\[[^\]]*\]\([^)]*\)/g, '[figure not included]')
        .replace(/<(script|style)[\s\S]*?<\/\1>/gi, '');

    // HTML structure to line breaks, then drop known tags only, so text
    // such as "x<y" in a math stem is never mistaken for markup.
    text = text
        .replace(/<!--[\s\S]*?-->/g, '')
        .replace(/<sup>\s*([^<]*?)\s*<\/sup>/gi, (_m, inner: string) =>
            superscript(inner),
        )
        .replace(/<br\s*\/?>/gi, '\n')
        .replace(/<li\b[^>]*>/gi, '\n- ')
        .replace(/<\/(p|div|li|ul|ol|h[1-6]|tr|table|blockquote|pre)>/gi, '\n')
        .replace(HTML_TAG, '');

    // Light Markdown that can wrap bank text. Underscores and single
    // asterisks are left alone: blanks (____) and math (3*4) use them.
    text = text
        .replace(/^\s{0,3}#{1,6}\s+/gm, '')
        .replace(/\*\*([^*\n]+)\*\*/g, '$1')
        .replace(/`([^`\n]+)`/g, '$1')
        .replace(/\[([^\]\n]+)\]\((?:[^)\s]+)\)/g, '$1');

    text = decodeEntities(text).replace(/\u00a0/g, ' ');

    return text
        .split('\n')
        .map((line) => line.replace(/[ \t]+/g, ' ').trimEnd())
        .join('\n')
        .replace(/^\n+|\n+$/g, '')
        .replace(/\n{3,}/g, '\n\n')
        .trim();
}

function oneLine(input: string | null | undefined): string {
    return toPlainText(input).replace(/\s*\n\s*/g, ' ');
}

/** A, B, C… for a display index (falls back to 1-based numbers past Z). */
export function optionLetter(displayIndex: number): string {
    return displayIndex >= 0 && displayIndex < 26
        ? String.fromCharCode(65 + displayIndex)
        : String(displayIndex + 1);
}

function isValidIndex(
    index: number | null | undefined,
    length: number,
): index is number {
    return (
        typeof index === 'number' &&
        Number.isInteger(index) &&
        index >= 0 &&
        index < length
    );
}

/** May the copy include the answer key, result and explanation? */
export function canIncludeAnswer(attempt: AiHandoffAttemptState): boolean {
    return attempt.revealed === true || attempt.mode === 'review';
}

export function buildAiHandoffText(
    question: AiHandoffQuestion,
    attempt: AiHandoffAttemptState,
    options: AiHandoffOptions = {},
): string {
    const lines: string[] = [];
    const displayOptions = Array.isArray(question.options)
        ? question.options
        : [];

    lines.push(`Philippine Civil Service Exam — ${attempt.examLevel}`);

    const category = oneLine(question.category);
    const topic = oneLine(question.subcategory);

    if (category) {
        lines.push(`Category: ${category}`);
    }

    if (topic) {
        lines.push(`Topic: ${topic}`);
    }

    lines.push('', 'Question:', toPlainText(question.stem), '');

    displayOptions.forEach((option, index) => {
        lines.push(`${optionLetter(index)}. ${oneLine(option)}`);
    });

    const selected = isValidIndex(
        attempt.selectedDisplayIndex,
        displayOptions.length,
    )
        ? attempt.selectedDisplayIndex
        : null;

    lines.push(
        '',
        `My answer: ${selected === null ? 'not answered yet' : optionLetter(selected)}`,
    );

    if (!canIncludeAnswer(attempt)) {
        lines.push('', AI_HANDOFF_HINT_PROMPT);

        return lines.join('\n');
    }

    const correct = isValidIndex(
        attempt.verifiedCorrectDisplayIndex,
        displayOptions.length,
    )
        ? attempt.verifiedCorrectDisplayIndex
        : null;

    const result: AiHandoffResult | null =
        attempt.result ??
        (selected === null
            ? 'Not answered'
            : correct === null
              ? null
              : selected === correct
                ? 'Correct'
                : 'Incorrect');

    if (result) {
        lines.push(`Result: ${result}`);
    }

    if (correct !== null) {
        lines.push(
            '',
            `Correct answer: ${optionLetter(correct)}. ${oneLine(displayOptions[correct])}`,
        );
    }

    const explanation = toPlainText(attempt.verifiedExplanation);

    if (explanation) {
        lines.push('', 'Civio explanation:', explanation);
    }

    const sourceRule = oneLine(question.source_rule);

    if (sourceRule) {
        lines.push('', `Source/rule: ${sourceRule}`);
    }

    const note = toPlainText(attempt.learnerNote);

    if (options.includeLearnerNote && note) {
        lines.push('', 'My note:', note);
    }

    lines.push('', AI_HANDOFF_EXPLAIN_PROMPT);

    return lines.join('\n');
}

/** Clipboard write with a hidden-textarea fallback for older browsers. */
export async function writeClipboardText(text: string): Promise<boolean> {
    if (typeof navigator !== 'undefined' && navigator.clipboard?.writeText) {
        try {
            await navigator.clipboard.writeText(text);

            return true;
        } catch {
            // Fall through to the textarea fallback (e.g. no permission).
        }
    }

    if (typeof document === 'undefined') {
        return false;
    }

    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.setAttribute('readonly', '');
    textarea.style.position = 'fixed';
    textarea.style.top = '-1000px';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();

    try {
        return document.execCommand('copy');
    } catch {
        return false;
    } finally {
        document.body.removeChild(textarea);
    }
}

export async function copyAiHandoff(
    question: AiHandoffQuestion,
    attempt: AiHandoffAttemptState,
    options: AiHandoffOptions = {},
): Promise<{ ok: boolean; text: string }> {
    const text = buildAiHandoffText(question, attempt, options);
    const ok = await writeClipboardText(text);

    return { ok, text };
}
