import type { Question } from '../types';

export const EXAM_CONSTANTS = {
    PROFESSIONAL_TIME_LIMIT_SECS: 11400,
    SUBPROFESSIONAL_TIME_LIMIT_SECS: 9600,
    PROFESSIONAL_TOTAL_ITEMS: 150, // was 170; demographics omitted for mocks
    SUBPROFESSIONAL_TOTAL_ITEMS: 145, // was 165; demographics omitted for mocks
    PROFESSIONAL_SCORED_ITEMS: 150,
    SUBPROFESSIONAL_SCORED_ITEMS: 145,
    DEMOGRAPHIC_QUESTION_COUNT: 20,
    /** Prefer previously-wrong items when filling a category block (local study bias). */
    WRONG_PRIORITY_PERCENTAGE: 0.5, // was 0.3 — more wrong/hard retries
    /** When filling unseen/seenCorrect, preferentially sample from harder half of pool. */
    HARD_BIAS_PERCENTAGE: 0.6,
    /** Near-duplicate stem skip: compare first N chars (normalized). */
    STEM_DEDUP_PREFIX_LEN: 48,
    /**
     * After unique stems are exhausted, still fill remaining quota with shuffled
     * variants (same stem family, different ids) so Professional can reach ~150.
     */
    FILL_VARIANTS_AFTER_UNIQUE: true,
    TIMER_RED_ZONE_SECS: 600,
    SHIELD_COOLDOWN_MS: 3000,
} as const;

export function isDemographicQuestion(q?: Partial<Question> | null): boolean {
    if (!q) {
        return false;
    }

    if (q.isDemographic) {
        return true;
    }

    if (!q.category) {
        return false;
    }

    const cat = q.category.toLowerCase();

    return cat === 'demographic profile' || cat.includes('demographic');
}

/** Stronger than Math.random when Web Crypto is available (browser / modern Node). */
function secureRandomUnit(): number {
    try {
        const cryptoObj =
            typeof globalThis !== 'undefined'
                ? (globalThis as { crypto?: Crypto }).crypto
                : undefined;

        if (cryptoObj?.getRandomValues) {
            const buf = new Uint32Array(1);
            cryptoObj.getRandomValues(buf);

            return buf[0] / (0xffffffff + 1);
        }
    } catch {
        // fall through
    }

    return Math.random();
}

export function fisherYatesShuffle<T>(array: T[]): T[] {
    const result = [...array];

    for (let i = result.length - 1; i > 0; i--) {
        const j = Math.floor(secureRandomUnit() * (i + 1));
        [result[i], result[j]] = [result[j], result[i]];
    }

    return result;
}

/**
 * Heuristic difficulty (no DB column). Higher = harder.
 * Biases Analytical/Numerical, longer stems, denser options/explanations, math-ish content.
 * Deprioritizes short Verbal clone-style stems.
 */
export function estimateDifficulty(q: Question): number {
    const stem = (q.stem || '').trim();
    const explanation = (q.explanation || '').trim();
    const options = Array.isArray(q.options) ? q.options : [];
    const cat = (q.category || '').toLowerCase();
    const sub = (q.subcategory || '').toLowerCase();

    let score = 0;

    // Category priors
    if (cat.includes('analytical')) {
        score += 28;
    } else if (cat.includes('numerical')) {
        score += 26;
    } else if (cat.includes('clerical')) {
        score += 12;
    } else if (cat.includes('general')) {
        score += 14;
    } else if (cat.includes('verbal')) {
        score += 6;
    }

    // Subcategory nudges
    if (
        /logic|assumption|conclusion|syllog|data interpretation|table|graph|abstract|spatial/.test(
            sub,
        )
    ) {
        score += 8;
    }

    if (/word analogy|synonym|antonym|vocabulary|spelling/.test(sub)) {
        score -= 4;
    }

    // Stem length / density
    const stemLen = stem.length;
    score += Math.min(22, Math.floor(stemLen / 40));

    if (stemLen < 60) {
        score -= 10; // easy short Verbal clones
    } else if (stemLen > 220) {
        score += 6;
    }

    // Options density
    const optChars = options.reduce((n, o) => n + String(o || '').length, 0);
    score += Math.min(12, Math.floor(optChars / 80));

    if (options.length >= 4) {
        const avgOpt = optChars / Math.max(1, options.length);

        if (avgOpt > 40) {
            score += 4;
        }
    }

    // Explanation richness (proxy for multi-step items)
    score += Math.min(10, Math.floor(explanation.length / 80));

    // Math-ish / quantitative cues in stem or options
    const mathBlob = `${stem} ${options.join(' ')}`;

    if (
        /\d/.test(mathBlob) &&
        /[%₱$]|ratio|percent|average|fraction|equation|solve|how many|what is \d/i.test(
            mathBlob,
        )
    ) {
        score += 10;
    }

    if (/[÷×√∑]|\\frac|\^|\d+\s*[+\-*/]\s*\d+/.test(mathBlob)) {
        score += 6;
    }

    // Passage / comprehension cues
    if (/according to|passage|paragraph|the author|main idea|inferred/i.test(stem)) {
        score += 8;
    }

    // Slight deprioritize explicit (variant N) clones when unique stems remain
    if (/\(variant\s*\d+\)/i.test(stem)) {
        score -= 8;
    }

    return score;
}

/**
 * Shuffle, then preferentially take from the harder half/quartile with randomness
 * (not a fully deterministic hard-first sort).
 */
export function shuffleHardBiased<T extends Question>(
    pool: T[],
    hardBiasPercentage: number = EXAM_CONSTANTS.HARD_BIAS_PERCENTAGE,
): T[] {
    if (pool.length <= 1) {
        return [...pool];
    }

    const withNoise = pool.map((q) => ({
        q,
        key: estimateDifficulty(q) + secureRandomUnit() * 12,
    }));
    withNoise.sort((a, b) => b.key - a.key);

    const hardCount = Math.max(
        1,
        Math.ceil(withNoise.length * Math.min(1, Math.max(0, hardBiasPercentage))),
    );
    const hardHalf = withNoise.slice(0, hardCount).map((x) => x.q);
    const easyHalf = withNoise.slice(hardCount).map((x) => x.q);

    // Prefer hard: interleave shuffled hard-first with occasional easy inserts
    const hardShuf = fisherYatesShuffle(hardHalf);
    const easyShuf = fisherYatesShuffle(easyHalf);
    const out: T[] = [];
    let hi = 0;
    let ei = 0;

    while (hi < hardShuf.length || ei < easyShuf.length) {
        const preferHard =
            hi < hardShuf.length &&
            (ei >= easyShuf.length || secureRandomUnit() < hardBiasPercentage);

        if (preferHard) {
            out.push(hardShuf[hi++]);
        } else if (ei < easyShuf.length) {
            out.push(easyShuf[ei++]);
        } else {
            out.push(hardShuf[hi++]);
        }
    }

    return out;
}

export function stemDedupeKey(
    stem: string,
    prefixLen: number = EXAM_CONSTANTS.STEM_DEDUP_PREFIX_LEN,
): string {
    return (stem || '')
        .toLowerCase()
        .replace(/\s*\(variant\s*\d+\)\s*/gi, ' ')
        .replace(/\s+/g, ' ')
        .trim()
        .slice(0, prefixLen);
}

/** Skip near-duplicate stems when assembling a picked list (keeps first occurrence). */
export function dedupeNearDuplicateStems<T extends Question>(
    items: T[],
    prefixLen: number = EXAM_CONSTANTS.STEM_DEDUP_PREFIX_LEN,
): T[] {
    const seen = new Set<string>();
    const out: T[] = [];

    for (const q of items) {
        const key = stemDedupeKey(q.stem, prefixLen);

        if (!key) {
            out.push(q);
            continue;
        }

        if (seen.has(key)) {
            continue;
        }

        seen.add(key);
        out.push(q);
    }

    return out;
}

/**
 * Prefer non-variant / unique-stem items first; keep variants for fill-to-quota.
 */
export function preferUniqueStemsFirst<T extends Question>(pool: T[]): T[] {
    const unique: T[] = [];
    const variants: T[] = [];

    for (const q of pool) {
        if (/\(variant\s*\d+\)/i.test(q.stem || '')) {
            variants.push(q);
        } else {
            unique.push(q);
        }
    }

    return [...unique, ...variants];
}

export async function apiPost<T = any>(url: string, payload: any): Promise<T> {
    const csrfToken =
        typeof document !== 'undefined'
            ? (
                  document.querySelector(
                      'meta[name="csrf-token"]',
                  ) as HTMLMetaElement
              )?.content || ''
            : '';

    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            'X-CSRF-TOKEN': csrfToken,
        },
        body: JSON.stringify(payload),
    });

    if (!res.ok) {
        throw new Error(
            `API request to ${url} failed with status ${res.status}`,
        );
    }

    return res.json();
}
