import { Card } from "../Card";
import { FaFileLines, FaPlay, FaBullseye, FaAngleDown, FaCaretUp, FaCaretDown, FaClock, FaFire, FaLayerGroup } from "react-icons/fa6";
import "./ProgressCard.css";
import type { JSX, ReactNode } from "react";
import type { ProgressMetric, MetricType } from "../../features/progress";

/**
 * Properties for the ProgressCard component
 */
export interface ProgressCardProps {
    /** The metrics to display in the card */
    metrics: ProgressMetric[];
    /** The currently selected time period filter */
    timePeriod?: string;
}

/**
 * Helper to get the correct icon and color class for a metric type
 */
const getMetricConfig = (type: MetricType): { icon: ReactNode, colorClass: string } => {
    switch (type) {
        case 'notes':
            return { icon: <FaFileLines />, colorClass: 'bg-blue' };
        case 'practice':
            return { icon: <FaPlay />, colorClass: 'bg-purple' };
        case 'accuracy':
            return { icon: <FaBullseye />, colorClass: 'bg-red' };
        case 'time':
            return { icon: <FaClock />, colorClass: 'bg-blue' };
        case 'streak':
            return { icon: <FaFire />, colorClass: 'bg-red' };
        case 'flashcards':
            return { icon: <FaLayerGroup />, colorClass: 'bg-purple' };
        default:
            return { icon: <FaFileLines />, colorClass: 'bg-blue' };
    }
};

export const ProgressCard = ({ 
    metrics, 
    timePeriod = "This Month" 
}: ProgressCardProps): JSX.Element => {
    return (
        <Card variant="default" className="progress-card">
            <div className="progress-header">
                <div className="progress-title">Your Progress</div>
                <div className="progress-filter">
                    {timePeriod} <FaAngleDown />
                </div>
            </div>
            
            <div className="progress-items">
                {metrics.slice(0, 3).map((metric) => {
                    const config = getMetricConfig(metric.type);
                    
                    return (
                        <div key={metric.id} className="progress-item">
                            <div className={`progress-icon ${config.colorClass}`}>
                                {config.icon}
                            </div>
                            <div className="progress-info">
                                <div className="progress-label">{metric.label}</div>
                                <div className="progress-value">{metric.value}</div>
                            </div>
                            <div className={`progress-trend ${metric.isPositive ? 'text-success' : 'text-danger'}`}>
                                {metric.isPositive ? <FaCaretUp /> : <FaCaretDown />} {metric.trend}%
                            </div>
                        </div>
                    );
                })}
            </div>

            <div className="progress-footer">
                <a href="#" className="view-all-link">View All</a>
            </div>
        </Card>
    );
};
