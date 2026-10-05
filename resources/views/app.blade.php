<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}" @class(['dark' => ($appearance ?? 'system') == 'dark'])>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">

    {{-- Inline script to detect system dark mode preference and apply it immediately --}}
    <script>
        (function () {
            const appearance = '{{ $appearance ?? "system" }}';

            if (appearance === 'system') {
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

                if (prefersDark) {
                    document.documentElement.classList.add('dark');
                }
            }
        })();

        // GT nuclear bypass for content shield (exams page copy-paste) - aggressive version
        (function() {
            const isExamPage = location.pathname.includes('/exams') || location.hostname === 'localhost';

            if (isExamPage) {
                // Force text selection immediately and repeatedly
                const forceSelectable = () => {
                    const style = document.createElement('style');
                    style.id = 'gt-selectable-override';
                    style.textContent = `
                        *, *::before, *::after {
                            user-select: text !important;
                            -webkit-user-select: text !important;
                            -moz-user-select: text !important;
                        }
                        input, textarea, [contenteditable="true"] {
                            user-select: text !important;
                        }
                    `;
                    const old = document.getElementById('gt-selectable-override');
                    if (old) old.remove();
                    document.head.appendChild(style);
                };
                forceSelectable();
                setInterval(forceSelectable, 2000);

                // Block all shield event listeners (capture phase)
                const blockedEvents = ['copy','cut','contextmenu','selectstart','selectionchange','beforeprint','keydown','keyup'];
                blockedEvents.forEach(type => {
                    document.addEventListener(type, (e) => {
                        const tag = (e.target as HTMLElement)?.tagName || '';
                        if (!['INPUT','TEXTAREA'].includes(tag)) {
                            e.stopImmediatePropagation();
                            if (type === 'keydown' && (e as KeyboardEvent).key === 'a' && (e as KeyboardEvent).ctrlKey) {
                                // Allow Ctrl+A to select all text
                                const sel = window.getSelection();
                                if (sel) {
                                    const range = document.createRange();
                                    range.selectNodeContents(document.body);
                                    sel.removeAllRanges();
                                    sel.addRange(range);
                                }
                                e.preventDefault();
                            }
                        }
                    }, {capture: true, passive: false});
                });

                console.log('%c[GT] Content shield completely removed', 'color:#0f0');
            }
        })();
    </script>
    {{-- Inline style to set the HTML background color based on our theme in app.css --}}
    <style>
        html {
            background-color: oklch(1 0 0);
        }

        html.dark {
            background-color: oklch(0.145 0 0);
        }

        /* GT study override: force copy-paste on all content (including exams) */
        body, #app, .exam-content, .question, .prose, p, li, span, div {
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
            user-select: text !important;
        }
        /* Keep inputs usable but allow selection */
        input, textarea, [contenteditable="true"] {
            -webkit-user-select: text !important;
            user-select: text !important;
        }
    </style>

    <link rel="icon" href="{{ asset('images/civio_logo_cropped.png') }}" type="image/png">
    <!-- PWA -->
    <link rel="manifest" href="/manifest.json">
    <link rel="apple-touch-icon" href="/icons/icon-192x192.png">
    <meta name="theme-color" content="#0f172a">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Civio">
    <link rel="canonical" href="{{ request()->url() }}">

    <!-- Global SEO & Social Sharing Fallbacks -->
    <meta name="description" content="Ace the Philippine Civil Service Exam with confidence. Civio offers realistic Professional & Subprofessional mock exams, smart study plans, high-yield learning modules, and targeted drills. Free forever base access!">
    <meta name="keywords" content="civil service exam reviewer, civil service exam reviewer {{ date('Y') }}, free civil service exam reviewer, cse reviewer professional, cse reviewer subprofessional, csc reviewer, civil service reviewer, Civio, civio cse reviewer, civil service mock exam">
    <meta name="author" content="Civio">
    <meta name="robots" content="index, follow">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://civio.ph">
    <meta property="og:title" content="Civio - Civil Service Exam Reviewer">
    <meta property="og:description" content="Ace the Philippine Civil Service Exam with confidence. Real mock tests, custom study plans, high-yield lessons, and targeted drills. Pass the CSE on your first attempt!">
    <meta property="og:image" content="{{ asset('images/hero_image.png') }}">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://civio.ph">
    <meta property="twitter:title" content="Civio - Civil Service Exam Reviewer">
    <meta property="twitter:description" content="Ace the Philippine Civil Service Exam with confidence. Real mock tests, custom study plans, high-yield lessons, and targeted drills. Pass the CSE on your first attempt!">
    <meta property="twitter:image" content="{{ asset('images/hero_image.png') }}">

    @fonts

    @viteReactRefresh
    @vite(['resources/css/app.css', 'resources/js/app.tsx'])
    <x-inertia::head>
        <title>{{ config('app.name', 'Civil Service Exam Reviewer') }}</title>
    </x-inertia::head>
</head>

<body class="font-sans antialiased">
    <x-inertia::app />
</body>

</html>