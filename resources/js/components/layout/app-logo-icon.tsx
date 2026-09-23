import type { ImgHTMLAttributes } from 'react';

export default function AppLogoIcon({
    className,
    ...props
}: ImgHTMLAttributes<HTMLImageElement>) {
    return (
        <img
            src="/images/hiraya_logo_cropped.png"
            alt="CIVIO Logo"
            className={className}
            {...props}
        />
    );
}
