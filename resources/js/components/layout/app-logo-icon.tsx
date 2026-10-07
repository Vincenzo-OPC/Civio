import type { ImgHTMLAttributes } from 'react';

type AppLogoIconProps = Omit<ImgHTMLAttributes<HTMLImageElement>, 'src'>;

/** Civio mark (neutral placeholder): violet tile, lime "C" and dot. */
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
