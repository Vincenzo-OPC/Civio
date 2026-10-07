import { usePage } from '@inertiajs/react';
import { useEffect, useMemo, useState, useRef } from 'react';
import { toast } from 'sonner';
import { AnnouncementsBanner } from '@/components/domain/announcements-banner';
import { AppContent } from '@/components/layout/app-content';
import { AppShell } from '@/components/layout/app-shell';
import { AppSidebar } from '@/components/layout/app-sidebar';
import { AppSidebarHeader } from '@/components/layout/app-sidebar-header';
import SiteFooter from '@/components/layout/site-footer';
import SiteHeader from '@/components/layout/site-header';
import { CookieConsentBanner } from '@/components/shared/cookie-consent-banner';
import TermsAcceptanceGuard from '@/components/shared/terms-acceptance-guard';
import { connectRealtime } from '@/lib/realtime';
import type { RealtimeConfig } from '@/lib/realtime';
import type { AppLayoutProps } from '@/types';

export default function AppSidebarLayout({
    children,
    breadcrumbs = [],
}: AppLayoutProps) {
    const { auth, pusher, pending_feedback_count } = usePage().props as any;
    const { url } = usePage();
    const [isWaitingForAi, setIsWaitingForAi] = useState(() => {
        if (typeof window !== 'undefined') {
            return localStorage.getItem('waiting_for_ai') === 'true';
        }

        return false;
    });
    const [feedbackCount, setFeedbackCount] = useState(
        pending_feedback_count || 0,
    );
    const isAdmin = auth.user?.role === 'admin';
    // Realtime (Echo + Pusher) is loaded on demand: only for admins (feedback
    // badge) or while an admin AI generation is pending. See lib/realtime.ts.
    const pusherKey: string | undefined = pusher?.key;
    const pusherCluster: string | undefined = pusher?.cluster;
    const pusherHost: string | undefined = pusher?.host;
    const pusherPort: number | undefined = pusher?.port;
    const pusherScheme: string | undefined = pusher?.scheme;
    const realtimeConfig = useMemo<RealtimeConfig | null>(
        () =>
            pusherKey
                ? {
                      key: pusherKey,
                      cluster: pusherCluster,
                      host: pusherHost,
                      port: pusherPort,
                      scheme: pusherScheme,
                  }
                : null,
        [pusherKey, pusherCluster, pusherHost, pusherPort, pusherScheme],
    );
    const prevPendingCountRef = useRef(pending_feedback_count);

    // Reset feedback count when page props change (after Inertia requests)
    useEffect(() => {
        if (prevPendingCountRef.current !== pending_feedback_count) {
            setFeedbackCount(pending_feedback_count || 0);
            prevPendingCountRef.current = pending_feedback_count;
        }
    }, [pending_feedback_count]);

    useEffect(() => {
        // Listen for same-tab triggers
        const handleAiStart = () => setIsWaitingForAi(true);
        window.addEventListener('ai_generation_started', handleAiStart);

        return () =>
            window.removeEventListener('ai_generation_started', handleAiStart);
    }, []);

    // Listen for new feedback submissions (admin only)
    useEffect(() => {
        if (!auth.user || !isAdmin || !realtimeConfig) {
            return;
        }

        return connectRealtime(realtimeConfig, (echo) => {
            echo.channel('admin-notifications').listen(
                'NewFeedbackSubmitted',
                (e: any) => {
                    // Do not show the admin notification toast to the user who just submitted it
                    if (!e.feedback || e.feedback.user_id != auth.user.id) {
                        toast.success('New feedback submitted', {
                            duration: 8000,
                            description:
                                'A user has reported content that needs review.',
                            action: {
                                label: 'View',
                                onClick: () => {
                                    window.location.href = '/admin/feedbacks';
                                },
                            },
                        });
                    }

                    // Update feedback count
                    setFeedbackCount((prev: number) => prev + 1);

                    // Dispatch event for sidebar to update
                    window.dispatchEvent(
                        new CustomEvent('new_feedback_submitted', {
                            detail: e,
                        }),
                    );
                },
            );

            return () => {
                echo.leaveChannel('admin-notifications');
                echo.disconnect();
            };
        });
    }, [auth.user, isAdmin, realtimeConfig]);

    // Listen for feedback status changes to update count
    useEffect(() => {
        const handleStatusChanged = (e: CustomEvent) => {
            const { currentStatus, newStatus } = e.detail;

            if (currentStatus === 'pending' && newStatus !== 'pending') {
                // Changed from pending to resolved/dismissed - decrement
                setFeedbackCount((prev: number) => Math.max(0, prev - 1));
            } else if (currentStatus !== 'pending' && newStatus === 'pending') {
                // Changed from resolved/dismissed to pending - increment
                setFeedbackCount((prev: number) => prev + 1);
            }
        };

        const handleCountRefresh = () => {
            // Reload page to get fresh count from server
            window.location.reload();
        };

        window.addEventListener(
            'feedback_status_changed',
            handleStatusChanged as EventListener,
        );
        window.addEventListener(
            'feedback_count_refresh',
            handleCountRefresh as EventListener,
        );

        return () => {
            window.removeEventListener(
                'feedback_status_changed',
                handleStatusChanged as EventListener,
            );
            window.removeEventListener(
                'feedback_count_refresh',
                handleCountRefresh as EventListener,
            );
        };
    }, []);

    useEffect(() => {
        if (!auth.user || !isWaitingForAi || !realtimeConfig) {
            return;
        }

        // Only instantiate and connect when actually waiting for AI
        return connectRealtime(realtimeConfig, (echo) => {
            echo.private(`App.Models.User.${auth.user.id}`)
                .listen('AiGenerationCompleted', (e: any) => {
                    toast.success(e.message, {
                        duration: 8000,
                        action: {
                            label: 'View Drafts',
                            onClick: () => {
                                window.location.href =
                                    e.type === 'module'
                                        ? '/admin/learn/drafts'
                                        : '/admin/questions/drafts';
                            },
                        },
                    });

                    // Disconnect and clean up once received
                    localStorage.removeItem('waiting_for_ai');
                    setIsWaitingForAi(false);
                    echo.disconnect();

                    // Notify forms that AI is done so they can update their loading state
                    window.dispatchEvent(new Event('ai_generation_completed'));
                })
                .listen('AiGenerationFailed', (e: any) => {
                    toast.error(e.message, {
                        duration: 8000,
                    });

                    // Disconnect and clean up on error
                    localStorage.removeItem('waiting_for_ai');
                    setIsWaitingForAi(false);
                    echo.disconnect();

                    // Dispatch failure event
                    window.dispatchEvent(new Event('ai_generation_failed'));
                });

            return () => {
                echo.disconnect();
            };
        });
    }, [auth.user, isWaitingForAi, realtimeConfig]);

    if (!auth.user) {
        const activeNav = url.startsWith('/learn')
            ? 'learn'
            : url.startsWith('/guide')
              ? 'guide'
              : '';

        return (
            <div className="flex min-h-screen flex-col bg-slate-50/30 dark:bg-slate-950/20">
                <SiteHeader activeNav={activeNav} />
                <main className="flex-1 px-4 py-12 sm:px-6">{children}</main>
                <SiteFooter />
                <CookieConsentBanner />
            </div>
        );
    }

    return (
        <TermsAcceptanceGuard>
            <AppShell variant="sidebar">
                <AppSidebar feedbackCount={feedbackCount} />
                <AppContent variant="sidebar" className="overflow-x-hidden">
                    <AppSidebarHeader breadcrumbs={breadcrumbs} />
                    <AnnouncementsBanner />
                    {children}
                </AppContent>
            </AppShell>
            <CookieConsentBanner />
        </TermsAcceptanceGuard>
    );
}
