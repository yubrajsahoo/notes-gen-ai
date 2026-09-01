/**
 * Defines the type of metric being tracked.
 * Used by UI components to map to specific icons and colors.
 */
export type MetricType = 'notes' | 'practice' | 'accuracy' | 'time' | 'streak' | 'flashcards';

/**
 * Represents a single progress metric for a user.
 */
export interface ProgressMetric {
    /** Unique identifier for the metric */
    id: string;
    /** Type of metric for UI mapping */
    type: MetricType;
    /** Display label (e.g., 'Notes Created') */
    label: string;
    /** The actual value to display (e.g., '18' or '78%') */
    value: string | number;
    /** The trend percentage value (e.g., 20 for 20%) */
    trend: number;
    /** Whether the trend is positive (upwards) or negative (downwards) */
    isPositive: boolean;
}
