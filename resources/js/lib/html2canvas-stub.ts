/**
 * jsPDF imports `html2canvas` only for `doc.html()`.
 * Civio already captures pages with `html2canvas-pro` and embeds the JPEG.
 * Shipping both libraries costs about 40 kB brotli and is unused.
 */
export default function html2canvas(): Promise<never> {
    return Promise.reject(
        new Error(
            'html2canvas is not included. PDF export uses html2canvas-pro.',
        ),
    );
}
