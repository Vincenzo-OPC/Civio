import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { bindFlushListeners } from '../../resources/js/pages/user/exams/utils/flush-listeners';

class FakeTarget extends EventTarget {
    visibilityState = 'visible';
}

describe('bindFlushListeners', () => {
    it('flushes on pagehide and when the page becomes hidden', () => {
        const win = new FakeTarget();
        const doc = new FakeTarget();
        let calls = 0;
        bindFlushListeners(win, doc, () => calls++);

        win.dispatchEvent(new Event('pagehide'));
        doc.visibilityState = 'hidden';
        doc.dispatchEvent(new Event('visibilitychange'));

        assert.equal(calls, 2);
    });

    it('removes every listener, including visibilitychange, on cleanup', () => {
        const win = new FakeTarget();
        const doc = new FakeTarget();
        let calls = 0;
        const unbind = bindFlushListeners(win, doc, () => calls++);
        unbind();

        win.dispatchEvent(new Event('pagehide'));
        win.dispatchEvent(new Event('beforeunload'));
        doc.visibilityState = 'hidden';
        doc.dispatchEvent(new Event('visibilitychange'));

        assert.equal(calls, 0);
    });
});
