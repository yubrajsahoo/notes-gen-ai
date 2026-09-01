import "./Card.css";

import type {ReactNode} from "react";

/**
 * Properties for the Card component.
 */
export interface CardProps {
    /** Optional title displayed prominently in the card body */
    title?: ReactNode;
    /** Optional subtitle displayed below the title */
    subtitle?: ReactNode;
    /** URL source for an image displayed at the top of the card */
    image?: string;
    /** Alternative text for the image */
    imageAlt?: string;
    /** Optional icon element displayed in the card */
    icon?: ReactNode;
    /** Optional content for the card header section */
    header?: ReactNode;
    /** Optional content for the card footer section */
    footer?: ReactNode;
    /** Content to be rendered inside the card body */
    children?: ReactNode;
    /** Optional prefix used for custom BEM-like class names (e.g. prefix-card) */
    prefix?: string;
    /** The predefined design variant to use */
    variant?: 'default' | 'primary' | 'secondary' | 'outline';
    /** Additional CSS classes to apply to the card container */
    className?: string;
}

/**
 * A generic and reusable Card component.
 * Can be customized using the prefix prop to scope specific styles.
 *
 * @param {CardProps} props - The card properties.
 * @returns {JSX.Element} The rendered card component.
 */
export const Card = ({
                         title,
                         subtitle,
                         image,
                         imageAlt = "Card image",
                         icon,
                         header,
                         footer,
                         children,
                         prefix = "",
                         variant = "default",
                         className = "",
                     }: CardProps) => {
        return (
            <>
                <div className={`card card-${variant} ${prefix ? `${prefix}-card` : ''} ${className}`}>

                    {header && <div className={`card-header ${prefix}-card-header`}>{header}</div>}

                    {image && <img src={image} className={`card-image-top ${prefix}-card-img-top`} alt={imageAlt}/>}
                    {icon && <div className={`card-icon ${prefix}-card-icon`}>{icon}</div>}


                    <div className={`card-body ${prefix}-card-body`}>
                        {title && <div className={`card-title ${prefix}-card-title`}>{title}</div>}
                        {subtitle && <div className={`card-subtitle ${prefix}-card-subtitle`}>{subtitle}</div>}
                        {children && <div className={`card-text ${prefix}-card-text`}>{children}</div>}
                    </div>

                    {footer && <div className={`card-footer ${prefix}card-footer`}>{footer}</div>}
                </div>
            </>
        );
    }
;
