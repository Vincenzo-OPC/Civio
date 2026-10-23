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
            src="/images/civio-icon-320.png"
            alt={alt}
            width={320}
            height={176}
            decoding="async"
            className={`object-contain ${className ?? ''}`}
            {...props}
        />
    );
}
