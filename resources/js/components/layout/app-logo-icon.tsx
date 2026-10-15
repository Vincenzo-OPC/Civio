import type { ImgHTMLAttributes } from 'react';

type AppLogoIconProps = Omit<ImgHTMLAttributes<HTMLImageElement>, 'src'>;

/** Civio mark: violet tile, paper C. Lime is not used on the logo. */
export default function AppLogoIcon({
    alt = 'Civio logo',
    ...props
}: AppLogoIconProps) {
    return (
        <img
            src="/images/civio-mark.svg"
            alt={alt}
            width={512}
            height={512}
            {...props}
        />
    );
}
