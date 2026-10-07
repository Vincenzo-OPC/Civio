import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
    applyLiteClass,
    detectLite,
    parsePreference,
    resolveLite,
    shouldRegisterServiceWorker,
} from '../../resources/js/lib/lite-mode';

describe('detectLite', () => {
    it('turns on for Save-Data and slow connections', () => {
        assert.equal(detectLite({ saveData: true, effectiveType: '4g' }), true);
        assert.equal(detectLite({ effectiveType: 'slow-2g' }), true);
        assert.equal(detectLite({ effectiveType: '2g' }), true);
        assert.equal(detectLite({ effectiveType: '3g' }), true);
    });

    it('stays off for fast or unknown connections', () => {
        assert.equal(detectLite({ effectiveType: '4g' }), false);
        assert.equal(detectLite({}), false);
        assert.equal(detectLite(null), false);
        assert.equal(detectLite(undefined), false);
    });
});

describe('resolveLite', () => {
    it('lets a manual choice beat the connection', () => {
        assert.equal(resolveLite('on', { effectiveType: '4g' }), true);
        assert.equal(resolveLite('off', { saveData: true }), false);
        assert.equal(resolveLite('auto', { effectiveType: '3g' }), true);
        assert.equal(resolveLite('auto', { effectiveType: '4g' }), false);
    });

    it('treats anything unknown as auto', () => {
        assert.equal(parsePreference('on'), 'on');
        assert.equal(parsePreference('off'), 'off');
        assert.equal(parsePreference('yes'), 'auto');
        assert.equal(parsePreference(null), 'auto');
    });
});

describe('applyLiteClass', () => {
    it('adds and removes the lite class', () => {
        const classes = new Set<string>();
        const el = {
            classList: {
                toggle: (name: string, force?: boolean) => {
                    if (force) {
                        classes.add(name);
                    } else {
                        classes.delete(name);
                    }

                    return Boolean(force);
                },
            },
        };

        applyLiteClass(el, true);
        assert.equal(classes.has('lite'), true);
        applyLiteClass(el, false);
        assert.equal(classes.has('lite'), false);
        applyLiteClass(null, true);
    });
});

describe('shouldRegisterServiceWorker', () => {
    it('skips the offline precache in Lite unless opted in', () => {
        assert.equal(shouldRegisterServiceWorker(false, false), true);
        assert.equal(shouldRegisterServiceWorker(true, false), false);
        assert.equal(shouldRegisterServiceWorker(true, true), true);
    });
});
