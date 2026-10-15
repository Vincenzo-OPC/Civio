<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}" @class(['dark' => ($appearance ?? 'system') == 'dark', 'lite' => request()->cookie('civio_lite') === '1'])>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">

    {{-- Inline scripts are plain JavaScript (no TypeScript): browsers run them as-is. tests/Feature/Views/AppInlineScriptTest.php checks this. --}}
    {{-- Detect system dark mode preference and apply it immediately --}}
    <script>
        (function () {
            var appearance = '{{ $appearance ?? "system" }}';

            if (appearance === 'system') {
                var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

                if (prefersDark) {
                    document.documentElement.classList.add('dark');
                }
            }
        })();
    </script>
    {{-- GT study override: keep text selectable and copyable on exam pages (and on localhost). --}}
    {{-- Only the copy/selection events are intercepted; keyboard events are left alone so dialogs, shortcuts and forms keep working. --}}
    <script>
        (function () {
            var isExamPage = location.pathname.indexOf('/exams') !== -1 || location.hostname === 'localhost';

            if (!isExamPage) {
                return;
            }

            var forceSelectable = function () {
                if (!document.head) {
                    return;
                }

                var old = document.getElementById('gt-selectable-override');

                if (old) {
                    old.remove();
                }

                var style = document.createElement('style');
                style.id = 'gt-selectable-override';
                style.textContent =
                    '*, *::before, *::after { user-select: text !important; -webkit-user-select: text !important; -moz-user-select: text !important; }' +
                    ' input, textarea, [contenteditable="true"] { user-select: text !important; }';
                document.head.appendChild(style);
            };
            forceSelectable();
            setInterval(forceSelectable, 2000);

            // Stop copy-blocking listeners (capture phase) everywhere except form fields.
            ['copy', 'cut', 'contextmenu', 'selectstart'].forEach(function (type) {
                document.addEventListener(type, function (e) {
                    var target = e.target;
                    var tag = target && target.tagName ? target.tagName : '';

                    if (tag !== 'INPUT' && tag !== 'TEXTAREA') {
                        e.stopImmediatePropagation();
                    }
                }, { capture: true });
            });
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

    <link rel="icon" href="/favicon.ico" sizes="48x48">
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <!-- PWA -->
    <link rel="manifest" href="/manifest.json">
    <link rel="apple-touch-icon" href="/icons/icon-192x192.png">
    <meta name="theme-color" content="#FAFAF7">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Civio">
    <link rel="canonical" href="{{ request()->url() }}">

    <!-- Global SEO & Social Sharing Fallbacks -->
    <meta name="description" content="Timed practice for the Philippine Civil Service Exam. Professional is 150 scored items in 3 hours 10 minutes. Subprofessional is 145 in 2 hours 40 minutes. Civio is not the Civil Service Commission.">
    <meta name="keywords" content="civil service exam reviewer, civil service exam reviewer {{ date('Y') }}, free civil service exam reviewer, cse reviewer professional, cse reviewer subprofessional, civil service reviewer, Civio, civil service mock exam">
    <meta name="author" content="Civio">
    <meta name="robots" content="index, follow">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://civio.ph">
    <meta property="og:title" content="Civio">
    <meta property="og:description" content="Timed practice for the Professional and Subprofessional exams. Civio is not the Civil Service Commission.">
    <meta property="og:image" content="{{ asset('images/hero_image.png') }}">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://civio.ph">
    <meta property="twitter:title" content="Civio">
    <meta property="twitter:description" content="Timed practice for the Professional and Subprofessional exams. Civio is not the Civil Service Commission.">
    <meta property="twitter:image" content="{{ asset('images/hero_image.png') }}">

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