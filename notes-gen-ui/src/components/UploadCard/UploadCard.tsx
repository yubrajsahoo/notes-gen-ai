import { Card, Button } from "../index";
import { FaCloudArrowUp } from "react-icons/fa6";
import "./UploadCard.css";
import type { JSX } from "react";

/**
 * Properties for the UploadCard component.
 */
export interface UploadCardProps {
    /** Callback fired when the 'Upload File' button is clicked */
    onUpload?: () => void;
}

/**
 * A specialized Card component for the "Upload Recording" action.
 * Pre-configured with the cloud upload icon, specific copy, and default styling.
 *
 * @param {UploadCardProps} props - The upload card properties
 * @returns {JSX.Element} The rendered UploadCard component.
 */
export const UploadCard = ({ onUpload }: UploadCardProps): JSX.Element => {
    return (
        <Card
            icon={<FaCloudArrowUp />}
            title="Upload Recording"
            subtitle="Upload an audio or video file and generate notes."
            prefix="upload"
            variant="default"
        >
            <Button type="button" variant="outline" onClick={onUpload}>
                Upload File
            </Button>
        </Card>
    );
};
