/** Lite L2 offline drill packs: shapes shared by the API, store and runner. */
import type { CategoryScore } from '@/pages/user/exams/types';

/** One item as served by GET /offline/packs/{category}. Original option order. */
export interface OfflinePackItem {
    id: number;
    stem: string;
    options: string[];
    correct_option: number;
    explanation: string;
    category: string;
    subcategory: string;
    language: string;
}

export interface OfflineSubcategorySummary {
    id: number;
    name: string;
    items: number;
    pages: number;
    version: string;
    bytes: number;
}

export interface OfflinePackSummary {
    category_id: number;
    category: string;
    items: number;
    pages: number;
    version: string;
    bytes: number;
    subcategories: OfflineSubcategorySummary[];
}

export interface OfflineManifest {
    packs: OfflinePackSummary[];
    per_page: number;
    version: string;
}

export interface OfflinePackPage {
    category_id: number;
    subcategory_id: number | null;
    page: number;
    pages: number;
    per_page: number;
    total: number;
    version: string;
    items: OfflinePackItem[];
}

/** A downloaded pack as kept in IndexedDB. */
export interface StoredPack {
    categoryId: number;
    category: string;
    version: string;
    bytes: number;
    downloadedAt: string;
    items: OfflinePackItem[];
}

/** One answer waiting to be synced (indices are original option order). */
export interface QueuedAnswer {
    client_id: string;
    question_id: number;
    selected_option: number;
    claimed_correct_option: number;
    pack_version: string | null;
    answered_at: string;
}

export interface SyncVerdict {
    client_id: string;
    question_id: number;
    status: 'accepted' | 'rejected';
    reason: string | null;
    duplicate: boolean;
    correct?: boolean;
}

export interface SyncResponse {
    success: boolean;
    results: SyncVerdict[];
    bias: {
        wrong_ids: number[];
        correct_ids: number[];
        category_scores: Record<string, CategoryScore> | unknown[];
    };
}
