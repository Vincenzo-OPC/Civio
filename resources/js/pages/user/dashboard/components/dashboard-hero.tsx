import { Link } from '@inertiajs/react';
import { ChevronDown, Play, GraduationCap } from 'lucide-react';
import React from 'react';
import LiteModeToggle from '@/components/shared/lite-mode-toggle';
import { Button } from '@/components/ui/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { index as examsIndex } from '@/routes/exams';
import type { DashboardStats } from '../types';

interface DashboardHeroProps {
    firstName: string;
    /** Kept for callers; the exam date now lives in ExamCountdown. */
    stats?: DashboardStats | null;
    motivationText?: string | null;
    streak?: number;
}

export function DashboardHero({
    firstName,
    motivationText,
    streak = 0,
}: DashboardHeroProps) {
    const defaultMotivation =
        'Practice scores on this page are not a Civil Service Commission rating.';
    const motivation = motivationText || defaultMotivation;

    return (
        <div className="rounded-2xl border border-[#E3E5EA] bg-[#FAFAF7] p-5 sm:p-7 dark:border-slate-800 dark:bg-slate-900">
            <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
                <div className="space-y-3">
                    <div className="flex flex-wrap items-center justify-between gap-2.5">
                        <div className="flex flex-wrap items-center gap-2.5">
                            <div className="inline-flex items-center rounded-full border border-[#E3E5EA] bg-white px-3 py-1 text-xs font-medium text-[#101426] dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200">
                                Practice
                            </div>

                            {streak > 0 && (
                                <div className="inline-flex items-center rounded-full border border-[#E3E5EA] bg-white px-3 py-1 text-xs font-medium text-[#101426] dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200">
                                    {streak} day streak
                                </div>
                            )}
                        </div>
                        <LiteModeToggle />
                    </div>

                    <div>
                        <h1 className="text-2xl font-semibold tracking-tight text-[#101426] sm:text-3xl dark:text-white">
                            Welcome back, {firstName}
                        </h1>
                        <p className="mt-1.5 max-w-2xl text-sm leading-relaxed text-slate-600 sm:text-base dark:text-slate-300">
                            {motivation}
                        </p>
                    </div>
                </div>

                <div className="flex flex-col gap-3 sm:flex-row sm:items-center lg:flex-col lg:items-end">
                    <div className="flex w-full gap-2 sm:w-auto">
                        <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                                <Button
                                    size="default"
                                    uppercase={false}
                                    className="w-full gap-2 bg-[#5B35F5] font-medium text-white hover:bg-[#3D20C8] sm:w-auto"
                                >
                                    <Play className="size-4" />
                                    <span>Open a mock</span>
                                    <ChevronDown className="size-3.5 opacity-70" />
                                </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent
                                align="end"
                                className="w-56 rounded-xl border border-[#E3E5EA] bg-white p-1.5 dark:border-slate-800 dark:bg-slate-950"
                            >
                                <DropdownMenuItem asChild>
                                    <Link
                                        href={
                                            examsIndex({
                                                query: {
                                                    start: 'professional',
                                                    from: '/dashboard',
                                                },
                                            }).url
                                        }
                                        className="flex cursor-pointer items-center justify-between rounded-lg px-3 py-2 text-sm text-[#101426] hover:bg-[#F4F5F2] dark:text-slate-200 dark:hover:bg-slate-900"
                                    >
                                        <div className="flex items-center gap-2">
                                            <GraduationCap className="size-4 text-[#5B35F5]" />
                                            <span>Professional</span>
                                        </div>
                                        <span className="text-xs text-slate-500">
                                            150 items
                                        </span>
                                    </Link>
                                </DropdownMenuItem>
                                <DropdownMenuItem asChild>
                                    <Link
                                        href={
                                            examsIndex({
                                                query: {
                                                    start: 'subprofessional',
                                                    from: '/dashboard',
                                                },
                                            }).url
                                        }
                                        className="flex cursor-pointer items-center justify-between rounded-lg px-3 py-2 text-sm text-[#101426] hover:bg-[#F4F5F2] dark:text-slate-200 dark:hover:bg-slate-900"
                                    >
                                        <div className="flex items-center gap-2">
                                            <GraduationCap className="size-4 text-[#5B35F5]" />
                                            <span>Subprofessional</span>
                                        </div>
                                        <span className="text-xs text-slate-500">
                                            145 items
                                        </span>
                                    </Link>
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                    </div>
                </div>
            </div>
        </div>
    );
}
