// Dev-only stand-in for the production nginx, used by perf measurements.
// `php artisan serve` sends static files uncompressed and with no validators,
// which makes cold and warm numbers meaningless. This proxy:
//  - serves real files under public/ itself, the way nginx `try_files $uri`
//    does, with gzip, ETag and Last-Modified (nginx defaults);
//  - adds the Cache-Control rules from conf/nginx/civio-cache.conf when
//    PERF_CACHE_RULES=1 (mirrors that file; keep the two in step);
//  - forwards everything else to PHP and gzips text responses.
// Node built-ins only.
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import process from 'node:process';
import zlib from 'node:zlib';

const TEXT =
    /^(text\/|application\/(json|javascript|xml|manifest\+json)|image\/svg)/;
const TYPES = {
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.ico': 'image/x-icon',
    '.webp': 'image/webp',
    '.woff2': 'font/woff2',
    '.txt': 'text/plain',
    '.webmanifest': 'application/manifest+json',
};

/** Same rules as conf/nginx/civio-cache.conf. */
export function cacheControlFor(urlPath) {
    if (urlPath.startsWith('/build/assets/')) {
        return 'public, max-age=31536000, immutable';
    }

    if (
        urlPath === '/build/manifest.json' ||
        urlPath.endsWith('.webmanifest') ||
        urlPath === '/manifest.json'
    ) {
        return 'no-cache';
    }

    if (/^\/(images|icons)\//.test(urlPath)) {
        return 'public, max-age=2592000';
    }

    if (
        /^\/(favicon\.(ico|svg)|apple-touch-icon\.png|robots\.txt)$/.test(
            urlPath,
        )
    ) {
        return 'public, max-age=86400';
    }

    return null;
}

export function startGzipProxy({
    listenPort,
    targetPort,
    host = '127.0.0.1',
    root = 'public',
    rules = process.env.PERF_CACHE_RULES === '1',
}) {
    const pub = path.resolve(root);
    const server = http.createServer((req, res) => {
        const urlPath = decodeURIComponent((req.url ?? '/').split('?')[0]);
        const file = path.join(pub, urlPath);
        const gz = String(req.headers['accept-encoding'] ?? '').includes(
            'gzip',
        );
        let stat = null;

        if (file.startsWith(pub + path.sep) && !urlPath.endsWith('.php')) {
            try {
                stat = fs.statSync(file);

                if (!stat.isFile()) {
                    stat = null;
                }
            } catch {
                stat = null;
            }
        }

        if (stat && (req.method === 'GET' || req.method === 'HEAD')) {
            const etag = `"${stat.mtimeMs.toString(16)}-${stat.size.toString(16)}"`;
            const type =
                TYPES[path.extname(file)] ?? 'application/octet-stream';
            const headers = {
                'content-type': type,
                etag,
                'last-modified': stat.mtime.toUTCString(),
            };
            const cc = rules ? cacheControlFor(urlPath) : null;

            if (cc) {
                headers['cache-control'] = cc;
            }

            if (req.headers['if-none-match'] === etag) {
                res.writeHead(304, headers);

                return res.end();
            }

            if (gz && TEXT.test(type)) {
                headers['content-encoding'] = 'gzip';
                headers.vary = 'Accept-Encoding';
                res.writeHead(200, headers);

                if (req.method === 'HEAD') {
                    return res.end();
                }

                return fs
                    .createReadStream(file)
                    .pipe(zlib.createGzip({ level: 6 }))
                    .pipe(res);
            }

            headers['content-length'] = stat.size;
            res.writeHead(200, headers);

            if (req.method === 'HEAD') {
                return res.end();
            }

            return fs.createReadStream(file).pipe(res);
        }

        const upstream = http.request(
            {
                host,
                port: targetPort,
                method: req.method,
                path: req.url,
                headers: {
                    ...req.headers,
                    host: `${host}:${listenPort}`,
                    'accept-encoding': 'identity',
                },
            },
            (up) => {
                const headers = { ...up.headers };

                if (
                    gz &&
                    TEXT.test(String(headers['content-type'] ?? '')) &&
                    up.statusCode !== 304 &&
                    req.method !== 'HEAD'
                ) {
                    delete headers['content-length'];
                    headers['content-encoding'] = 'gzip';
                    headers.vary = headers.vary
                        ? `${headers.vary}, Accept-Encoding`
                        : 'Accept-Encoding';
                    res.writeHead(up.statusCode ?? 200, headers);
                    up.pipe(zlib.createGzip({ level: 6 })).pipe(res);
                } else {
                    res.writeHead(up.statusCode ?? 200, headers);
                    up.pipe(res);
                }
            },
        );
        upstream.on('error', () => {
            res.writeHead(502);
            res.end();
        });
        req.pipe(upstream);
    });

    return new Promise((resolve) =>
        server.listen(listenPort, host, () => resolve(server)),
    );
}
