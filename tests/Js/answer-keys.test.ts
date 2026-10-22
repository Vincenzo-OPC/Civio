import assert from 'node:assert/strict';
import { test } from 'node:test';
import { publishAnswerKeys } from '../../resources/js/pages/user/exams/utils/answer-keys';

test('released keys reach the review screen by question id, with answers', () => {
    const target = new EventTarget();
    let detail: unknown = null;
    target.addEventListener('civio:exam-answer-keys', (e) => {
        detail = (e as CustomEvent).detail;
    });

    publishAnswerKeys(
        [
            { id: 7, correct_option: 2, explanation: 'Because.' },
            { id: 9, correct_option: 0 },
        ],
        { 7: 2, 9: 1 },
        target,
    );

    assert.deepEqual(detail, {
        keys: {
            7: { correct_option: 2, explanation: 'Because.' },
            9: { correct_option: 0, explanation: '' },
        },
        answers: { 7: 2, 9: 1 },
    });
});
