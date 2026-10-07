/**
 * Lite L0: decide which build files the service worker precaches.
 *
 * Instead of precaching every chunk (~1.27 MB), precache only the app shell and
 * the chunks statically imported by the critical routes below. Everything else
 * (admin, analytics charts, PDF export, rarely used pages) is cached at runtime
 * the first time it is used (see `resources/js/sw.ts`).
 *
 * Pure and Node-safe: used by `vite.config.ts` at build time and by tests.
 */

export interface ViteManifestChunk {
    file: string;
    imports?: string[];
    css?: string[];
}

export type ViteManifest = Record<string, ViteManifestChunk>;

/** Entry points and pages a phone needs to open Civio and start studying. */
export const PRECACHE_ROOTS: readonly string[] = [
    'resources/js/app.tsx',
    'resources/css/app.css',
    'resources/js/pages/public/welcome.tsx',
    'resources/js/pages/auth/login.tsx',
    'resources/js/pages/user/dashboard/index.tsx',
    'resources/js/pages/user/exams/index.tsx',
    'resources/js/pages/user/drills/index.tsx',
    // Lite L2: the offline drill runner must open with no network.
    'resources/js/pages/offline/index.tsx',
];

/** Files (relative to the build dir) reachable through static imports from the roots. */
export function collectCriticalFiles(
    manifest: ViteManifest,
    roots: readonly string[] = PRECACHE_ROOTS,
): Set<string> {
    const files = new Set<string>();
    const seen = new Set<string>();
    const stack = [...roots];

    while (stack.length > 0) {
        const key = stack.pop() as string;

        if (seen.has(key)) {
            continue;
        }

        seen.add(key);
        const chunk = manifest[key];

        if (!chunk) {
            continue;
        }

        files.add(chunk.file);
        chunk.css?.forEach((css) => files.add(css));
        chunk.imports?.forEach((imported) => stack.push(imported));
    }

    return files;
}

function normalise(url: string): string {
    return url.replace(/^\.?\//, '').replace(/^build\//, '');
}

/** Should this precache-manifest URL stay in the service worker precache? */
export function keepPrecacheEntry(
    url: string,
    critical: ReadonlySet<string>,
): boolean {
    const path = normalise(url);

    return critical.has(path);
}

/**
 * Absolute URL for a precache entry. The service worker is served from /sw.js,
 * so a relative entry like `assets/app.js` would resolve to /assets/app.js;
 * build files live under /build/.
 */
export function toBuildUrl(url: string): string {
    return `/build/${normalise(url)}`;
}
