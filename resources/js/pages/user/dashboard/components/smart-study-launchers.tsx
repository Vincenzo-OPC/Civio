import { Link } from '@inertiajs/react';
import type { LucideIcon } from 'lucide-react';
import {
    BookOpen,
    ChevronRight,
    ClipboardList,
    ListChecks,
    Target,
} from 'lucide-react';
import { index as drillsIndex } from '@/routes/drills';
import { index as examsIndex } from '@/routes/exams';
import { index as learnIndex } from '@/routes/learn';
import type { NextModuleItem } from '../types';
import { DashPanel } from './dash-panel';

interface SmartStudyLaunchersProps {
    nextModule?: NextModuleItem | null;
    primaryWeakness?: string | null;
}

interface Tile {
    key: string;
    href: string;
    icon: LucideIcon;
    title: string;
    detail: string;
    cta: string;
}

/** Four equal tiles: the same icon, title, line and action rhythm in each. */
export function SmartStudyLaunchers({
    nextModule,
    primaryWeakness,
}: SmartStudyLaunchersProps) {
    const tiles: Tile[] = [
        {
            key: 'drills',
            href: primaryWeakness
                ? '/drills/smart-weakness?from=/dashboard'
                : drillsIndex({ query: { from: '/dashboard' } }).url,
            icon: Target,
            title: 'Practice Drills',
            detail: primaryWeakness
                ? `Focus: ${primaryWeakness}`
                : 'Short sets by subtopic',
            cta: 'Start Drill',
        },
        {
            key: 'custom',
            href: '/drills?tab=custom&from=/dashboard',
            icon: ListChecks,
            title: 'Custom Drills',
            detail: 'Mix topics or saved sets',
            cta: 'Build Drill',
        },
        {
            key: 'learn',
            href: nextModule ? `/learn/${nextModule.slug}` : learnIndex().url,
            icon: BookOpen,
            title: 'Lessons',
            detail: nextModule?.title
                ? `Next: ${nextModule.title}`
                : 'Lessons for every subject',
            cta: 'Open Lessons',
        },
        {
            key: 'exams',
            href: examsIndex({ query: { from: '/dashboard' } }).url,
            icon: ClipboardList,
            title: 'Exam Simulation',
            detail: 'Study Mode or Exam Mode',
            cta: 'View Mocks',
        },
    ];

    return (
        <DashPanel
            id="study-tools-title"
            title="Study Tools"
            subtitle="Drills, lessons and full mocks."
            footer={
                <Link href="/guide" className="dash-link">
                    Reviewer Guide
                    <ChevronRight className="size-4" aria-hidden />
                </Link>
            }
        >
            <div className="grid flex-1 auto-rows-fr grid-cols-1 gap-3 @xs:grid-cols-2">
                {tiles.map((tile) => (
                    <Link
                        key={tile.key}
                        href={tile.href}
                        data-launcher-tile
                        className="dash-tile group flex min-w-0 items-center gap-3 p-3.5 transition-colors @xs:flex-col @xs:items-start @xs:gap-0 @xs:p-4"
                    >
                        <tile.icon
                            className="size-5 shrink-0 text-(--dash-mark)"
                            aria-hidden
                        />
                        <div className="min-w-0 flex-1 @xs:mt-3">
                            <h3 className="text-[15px] leading-5 font-semibold">
                                {tile.title}
                            </h3>
                            <p className="dash-muted mt-0.5 truncate text-[13px] leading-5">
                                {tile.detail}
                            </p>
                        </div>
                        <span className="dash-link shrink-0 text-[13px] @xs:mt-auto @xs:pt-3">
                            <span className="hidden @xs:inline">
                                {tile.cta}
                            </span>
                            <ChevronRight className="size-4" aria-hidden />
                        </span>
                    </Link>
                ))}
            </div>
        </DashPanel>
    );
}
