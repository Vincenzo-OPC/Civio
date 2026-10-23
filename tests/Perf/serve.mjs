// Starts `php artisan serve` and the gzip proxy in front of it.
import { spawn } from 'node:child_process';
import process from 'node:process';
import { startGzipProxy } from './gzip-proxy.mjs';

const appPort = Number(process.env.PERF_APP_PORT || 8144);
const proxyPort = Number(process.env.PERF_PROXY_PORT || 8145);
const php = spawn(
    'php',
    [
        'artisan',
        'serve',
        '--host=127.0.0.1',
        `--port=${appPort}`,
        '--no-reload',
    ],
    {
        env: { ...process.env, PHP_CLI_SERVER_WORKERS: '4' },
        stdio: 'inherit',
        },
);
await startGzipProxy({ listenPort: proxyPort, targetPort: appPort });
console.log(`[perf] gzip proxy :${proxyPort} -> php :${appPort}`);
const stop = () => {
    try {
        php.kill('SIGTERM');
    } catch {
        /* already gone */
    }

    process.exit(0);
};
process.on('SIGTERM', stop);
process.on('SIGINT', stop);
php.on('exit', (code) => process.exit(code ?? 1));
