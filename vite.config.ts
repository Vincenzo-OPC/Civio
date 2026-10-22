import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import inertia from '@inertiajs/vite';
import { wayfinder } from '@laravel/vite-plugin-wayfinder';
import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import laravel from 'laravel-vite-plugin';
import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';
import {
    collectCriticalFiles,
    keepPrecacheEntry,
    toBuildUrl,
} from './resources/js/lib/pwa-precache';
import type { ViteManifest } from './resources/js/lib/pwa-precache';

/**
 * The built CSS repeats the Tailwind palette in display-p3 and lab.
 * `@layer theme` already has the sRGB values. Those two blocks are about
 * 4 kB brotli and leave the 33 kB cap with no room.
 */
function dropWideGamutPalette(css: string): string {
    const markers = [
        '@supports (color:color(display-p3 0 0 0))',
        '@supports (color:lab(0% 0 0))',
    ];

    let output = css;

    for (const marker of markers) {
        let cursor = 0;
        let next = '';

        while (cursor < output.length) {
            const start = output.indexOf(marker, cursor);

            if (start < 0) {
                next += output.slice(cursor);
                break;
            }

            let depth = 0;
            let end = start;

            for (; end < output.length; end++) {
                const char = output[end];

                if (char === '{') {
                    depth++;
                } else if (char === '}') {
                    depth--;

                    if (depth === 0) {
                        end++;
                        break;
                    }
                }
            }

            next += output.slice(cursor, start);
            cursor = end;
        }

        output = next;
    }

    return output;
}

/**
 * Lite L0: precache only the app shell + critical routes (see
 * resources/js/lib/pwa-precache.ts). Falls back to the full list if the Vite
 * manifest is missing.
 */
function trimPrecache<T extends { url: string }>(entries: T[]) {
    const manifestPath = 'public/build/manifest.json';

    if (!existsSync(manifestPath)) {
        return { manifest: entries, warnings: [] };
    }

    const manifest = JSON.parse(
        readFileSync(manifestPath, 'utf8'),
    ) as ViteManifest;
    const critical = collectCriticalFiles(manifest);

    return {
        manifest: entries
            .filter((entry) => keepPrecacheEntry(entry.url, critical))
            .map((entry) => ({ ...entry, url: toBuildUrl(entry.url) })),
        warnings: [],
    };
}

export default defineConfig({
    resolve: {
        alias: [
            {
                // Exact match. A string alias would also catch html2canvas-pro.
                find: /^html2canvas$/,
                replacement: fileURLToPath(
                    new URL(
                        './resources/js/lib/html2canvas-stub.ts',
                        import.meta.url,
                    ),
                ),
            },
        ],
    },
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.tsx'],
            ssr: 'resources/js/ssr.tsx',
            refresh: true,
            // No web fonts: the CSS stacks (Inter/Outfit → system-ui) never used
            // the previously preloaded Instrument Sans files (Lite L0).
        }),
        inertia(),
        react({
            babel: {
                plugins: ['babel-plugin-react-compiler'],
            },
        }),
        tailwindcss(),
        {
            name: 'drop-wide-gamut-palette',
            apply: 'build',
            generateBundle(_options, bundle) {
                for (const item of Object.values(bundle)) {
                    if (
                        item.type !== 'asset' ||
                        !item.fileName.endsWith('.css')
                    ) {
                        continue;
                    }

                    const source =
                        typeof item.source === 'string'
                            ? item.source
                            : Buffer.from(item.source).toString('utf8');

                    item.source = dropWideGamutPalette(source);
                }
            },
        },
        wayfinder({
            formVariants: true,
        }),
        VitePWA({
            strategies: 'injectManifest',
            srcDir: 'resources/js',
            filename: 'sw.ts',
            registerType: 'prompt',
            injectRegister: false,
            // The file is built to public/build/sw.js but served by Laravel at
            // /sw.js (ServiceWorkerController), so it controls every page.
            // Registered at /build/sw.js its scope was /build/ and it never
            // controlled a page, so nothing worked offline.
            buildBase: '/',
            scope: '/',
            manifest: false, // keep public/manifest.json (Civio)
            // public/ files (icons, logo) are not globbed: the Laravel build has no
            // Vite publicDir. They load from the network like before.
            injectManifest: {
                globPatterns: ['**/*.{js,css,png,svg}'],
                maximumFileSizeToCacheInBytes: 4 * 1024 * 1024,
                manifestTransforms: [async (entries) => trimPrecache(entries)],
            },
            devOptions: {
                enabled: false,
            },
        }),
    ],

    build: {
        // Content-hashed filenames for aggressive caching
        rollupOptions: {
            output: {
                manualChunks(id) {
                    // Split React into its own chunk
                    if (
                        id.includes('node_modules/react') ||
                        id.includes('node_modules/react-dom') ||
                        id.includes('node_modules/scheduler')
                    ) {
                        return 'vendor-react';
                    }
                    // Split UI libraries (radix, shadcn dependencies)
                    if (
                        id.includes('node_modules/@radix-ui') ||
                        id.includes('node_modules/class-variance-authority') ||
                        id.includes('node_modules/clsx')
                    ) {
                        return 'vendor-ui';
                    }
                    // Split Inertia into its own chunk
                    if (id.includes('node_modules/@inertiajs')) {
                        return 'vendor-inertia';
                    }
                },
                // Ensure hashed filenames for cache-busting
                assetFileNames: 'assets/[name]-[hash][extname]',
                chunkFileNames: 'assets/[name]-[hash].js',
                entryFileNames: 'assets/[name]-[hash].js',
            },
        },
        // Enable CSS code splitting
        cssCodeSplit: true,
        // Target modern browsers for smaller output
        target: 'es2020',
        // Enable source maps for production debugging (optional)
        sourcemap: false,
    },
});
