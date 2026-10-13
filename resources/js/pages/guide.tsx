import { Head, usePage } from '@inertiajs/react';
import { ReviewerGuideTabs } from '@/components/domain/reviewer-guide-tabs';
import { PageContainer } from '@/components/layout/page-container';
import { PageHeader } from '@/components/layout/page-header';
import SiteFooter from '@/components/layout/site-footer';
import SiteHeader from '@/components/layout/site-header';
import AppLayout from '@/layouts/app-layout';
import type { Auth } from '@/types';

type PageProps = {
    auth: Auth;
};

export default function Guide() {
    const { auth } = usePage<PageProps>().props;
    const isLoggedIn = !!auth.user;

    const content = (
        <>
            <div className="mb-8 flex items-start gap-3">
                <PageHeader
                    title="Exam guide"
                    description="Professional is 150 items in 3 hours 10 minutes. Subprofessional is 145 items in 2 hours 40 minutes. The published general passing rating is at least 80.00."
                />
            </div>

            <ReviewerGuideTabs showActions={isLoggedIn} />
        </>
    );

    if (isLoggedIn) {
        return (
            <AppLayout breadcrumbs={Guide.layout.breadcrumbs}>
                <Head>
                    <title>Exam guide | Civio</title>
                    <meta
                        name="description"
                        content="Professional is 150 items in 3 hours 10 minutes. Subprofessional is 145 in 2 hours 40 minutes. Passing is a general rating of at least 80.00. Civio is not the Civil Service Commission."
                    />
                    <meta property="og:title" content="Exam guide | Civio" />
                    <meta
                        property="og:description"
                        content="Official item counts, time limits, and the published passing rating. Civio is not an official CSC reviewer."
                    />
                </Head>
                <PageContainer>{content}</PageContainer>
            </AppLayout>
        );
    }

    return (
        <>
            <Head>
                <title>Exam guide | Civio</title>
                <meta
                    name="description"
                    content="Professional is 150 items in 3 hours 10 minutes. Subprofessional is 145 in 2 hours 40 minutes. Passing is a general rating of at least 80.00. Civio is not the Civil Service Commission."
                />
                <meta property="og:title" content="Exam guide | Civio" />
                <meta
                    property="og:description"
                    content="Official item counts, time limits, and the published passing rating. Civio is not an official CSC reviewer."
                />
            </Head>
            <div className="flex min-h-screen flex-col bg-slate-50/30 dark:bg-slate-900/20">
                <SiteHeader activeNav="guide" />
                <main className="flex-1 px-4 py-12 sm:px-6">
                    <div className="mx-auto max-w-6xl space-y-8">
                        <div className="flex items-start gap-4 border-b border-border pb-6 md:items-center">
                            <PageHeader
                                title="Exam guide"
                                description="Professional is 150 items in 3 hours 10 minutes. Subprofessional is 145 items in 2 hours 40 minutes. The published general passing rating is at least 80.00."
                                className="flex-1"
                            />
                        </div>
                        <ReviewerGuideTabs showActions={isLoggedIn} />
                    </div>
                </main>
                <SiteFooter />
            </div>
        </>
    );
}

// Register layout configuration
Guide.layout = {
    breadcrumbs: [
        {
            title: 'Reviewer Guide',
            href: '/guide',
        },
    ],
};
