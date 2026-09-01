import type {ButtonHTMLAttributes, JSX, ReactNode} from "react";
import "./Button.css";

/**
 * Properties for the Button component.
 */
export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    /** The content to be rendered inside the button */
    children: ReactNode;
    /** The predefined design variant to use */
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'inverted';
    /** Optional prefix used for custom BEM-like class names (e.g. prefix-btn) */
    prefix?: string;
    /** If true, the button will stretch to 100% of its container's width */
    fullWidth?: boolean;
    /** Additional CSS classes to apply to the button */
    className?: string;
    /** Function to call when the button is clicked */
    onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

/**
 * A reusable Button component.
 * Supports multiple predefined design variants and a custom prefix for specific styling scopes.
 * Any standard HTML button attribute can also be passed.
 *
 * @param children the children element
 * @param variant the variant
 * @param prefix the prefix
 * @param fullWidth
 * @param className the class names
 * @param {ButtonProps} props - The button properties.
 * @returns {JSX.Element} The rendered button component.
 */
export const Button = ({
                           children,
                           variant = "primary",
                           prefix = "",
                           fullWidth = false,
                           className = "",
                           ...props
                       }: ButtonProps): JSX.Element => {
    return (
        <button
            className={`btn btn-${variant} ${fullWidth ? 'btn-full' : ''} ${prefix ? `${prefix}-btn` : ''} ${className}`}
            {...props}
        >
            {children}
        </button>
    );
};
