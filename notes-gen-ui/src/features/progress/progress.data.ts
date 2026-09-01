import type {ProgressMetric} from './progress.model';

/**
 * Data for the user's progress metrics this month.
 * Based on the design requirements.
 */
export const PROGRESS_METRICS: ProgressMetric[] = [
    {
        id: 'metric_notes',
        type: 'notes',
        label: 'Notes Created',
        value: 18,
        trend: 20,
        isPositive: true
    },
    {
        id: 'metric_practice',
        type: 'practice',
        label: 'Practice Sessions',
        value: 12,
        trend: 8,
        isPositive: true
    },
    {
        id: 'metric_accuracy',
        type: 'accuracy',
        label: 'Accuracy',
        value: '78%',
        trend: 12,
        isPositive: true
    },
    {
        id: 'metric_time',
        type: 'time',
        label: 'Time Spent',
        value: '12h',
        trend: 5,
        isPositive: true
    },
    {
        id: 'metric_streak',
        type: 'streak',
        label: 'Day Streak',
        value: 7,
        trend: 2,
        isPositive: true
    },
    {
        id: 'metric_flashcards',
        type: 'flashcards',
        label: 'Flashcards',
        value: 120,
        trend: 15,
        isPositive: true
    }
];
