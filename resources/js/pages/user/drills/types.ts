export interface Question {
    id: number;
    stem: string;
    options: string[];
<<<<<<< HEAD
    /** Only present on the learner's own custom questions. */
=======
>>>>>>> origin/main
    correct_option?: number;
    explanation?: string;
    category: string;
    subcategory: string;
    language: string;
    originalOptionIndices?: number[];
    isDemographic?: boolean;
    isCustom?: boolean;
}

export interface Subcategory {
    id: number;
    name: string;
}

export interface Category {
    id: number;
    name: string;
    subcategory: Subcategory[];
}

export interface SavedDrillSet {
    id: number;
    name: string;
    description?: string | null;
    color: string;
    questions_count: number;
    sample_categories?: string[];
    created_at?: string;
}

export interface DrillsProps {
    bankPage?: { current: number; last: number };
    questions: Question[];
    categories: Category[];
    savedDrillSets?: SavedDrillSet[];
    wrongQuestionIds?: number[];
    seenQuestionIds?: number[];
}
