import type { ImgHTMLAttributes } from 'react';

type AppLogoIconProps = Omit<ImgHTMLAttributes<HTMLImageElement>, 'src'>;

/** Square app mark. The wordmark lives in AppLogo. */
export default function AppLogoIcon({
    alt = 'Civio',
    className,
    ...props
}: AppLogoIconProps) {
    return (
        <img
            src="/images/civio-icon.png"
            alt={alt}
            width={1024}
            height={562}
            className={`object-contain ${className ?? ''}`}
            {...props}
        />
    );
}
