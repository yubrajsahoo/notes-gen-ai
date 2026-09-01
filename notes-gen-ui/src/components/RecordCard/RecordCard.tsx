import {Card, Button} from "../index";
import {FaMicrophoneLines} from "react-icons/fa6";
import "./RecordCard.css";
import type {JSX} from "react";

/**
 * Properties for the RecordCard component.
 */
export interface RecordCardProps {
    /** Callback fired when the 'Start Recording' button is clicked */
    onStartRecording?: () => void;
}

/**
 * A specialized Card component for the "Start Recording" action.
 * Pre-configured with the microphone icon, specific copy, and recording styling.
 *
 * @param {RecordCardProps} props - The record card properties
 * @returns {JSX.Element} The rendered RecordCard component.
 */
export const RecordCard = ({onStartRecording}: RecordCardProps): JSX.Element => {
    return (
        <Card
            icon={<FaMicrophoneLines/>}
            title="Start Recording"
            subtitle="Record your lecture, meeting or any session and let AI create smart notes for you."
            prefix="record"
            variant="primary"
        >
            <Button variant="inverted" onClick={onStartRecording}>Start Recording</Button>
        </Card>
    );
};
