import { Head, router } from '@inertiajs/react';
import { PageContainer } from '@/components/layout/page-container';
import { PageHeader } from '@/components/layout/page-header';

interface RecallRow {
    id: number;
    stem: string;
    note: string | null;
    category: string | null;
    subcategory: string | null;
    status: 'pending' | 'approved' | 'rejected';
    moderator_note: string | null;
    created_at: string;
    user?: { name: string; email: string } | null;
}

interface PageProps {
    recalls: {
        data: RecallRow[];
    };
    pending_count: number;
}

export default function RecalledQuestionsIndex({
    recalls,
    pending_count,
}: PageProps) {
    const setStatus = (id: number, status: RecallRow['status']) => {
        router.put(
            `/admin/recalled-questions/${id}/status`,
            { status },
            { preserveScroll: true },
        );
    };

    return (
        <>
            <Head title="Practice question queue" />
            <PageContainer>
                <PageHeader
                    title="I remember a question"
                    description={`${pending_count} waiting. Approving a paraphrase only marks the queue. It does not publish an official CSC item.`}
                />
                <div className="space-y-3">
                    {recalls.data.length === 0 && (
                        <p className="text-sm text-muted-foreground">
                            No paraphrases yet.
                        </p>
                    )}
                    {recalls.data.map((row) => (
                        <article
                            key={row.id}
                            className="rounded-2xl border border-border bg-card p-4"
                        >
                            <div className="mb-2 flex flex-wrap items-center gap-2 text-xs font-bold uppercase tracking-wide text-muted-foreground">
                                <span>{row.status}</span>
                                {row.subcategory && <span>{row.subcategory}</span>}
                                {row.user && <span>{row.user.email}</span>}
                            </div>
                            <p className="text-sm leading-relaxed text-foreground">
                                {row.stem}
                            </p>
                            {row.note && (
                                <p className="mt-2 text-xs text-muted-foreground">
                                    {row.note}
                                </p>
                            )}
                            <div className="mt-3 flex flex-wrap gap-2">
                                <button
                                    type="button"
                                    onClick={() => setStatus(row.id, 'approved')}
                                    className="cursor-pointer rounded-lg bg-emerald-600 px-3 py-1.5 text-xs font-bold text-white"
                                >
                                    Approve queue
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setStatus(row.id, 'rejected')}
                                    className="cursor-pointer rounded-lg border border-border px-3 py-1.5 text-xs font-bold"
                                >
                                    Reject
                                </button>
                            </div>
                        </article>
                    ))}
                </div>
            </PageContainer>
        </>
    );
}

RecalledQuestionsIndex.layout = {
    breadcrumbs: [
        { title: 'Admin', href: '/admin/dashboard' },
        { title: 'Practice queue', href: '/admin/recalled-questions' },
    ],
};
