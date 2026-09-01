import { RecordCard, UploadCard } from "../index";
import "./RecordingQuickActions.css";

/**
 * A reusable container component that groups the RecordCard and UploadCard together.
 * Implements a responsive grid layout to handle different screen sizes perfectly.
 *
 * @returns {JSX.Element} The rendered RecordingQuickActions component.
 */
export const RecordingQuickActions = () => {
    return (
        <div className="recording-quick-actions">
            <div>
                <RecordCard />
            </div>
            <div>
                <UploadCard />
            </div>
        </div>
    );
};
