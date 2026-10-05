import type { ImgHTMLAttributes } from 'react';

export default function AppLogoIcon({
    className,
    ...props
}: ImgHTMLAttributes<HTMLImageElement>) {
    return (
        <img
            src="/images/civio_logo_cropped.png"
            alt="Civio Logo"
            className={className}
            {...props}
        />
    );
}
