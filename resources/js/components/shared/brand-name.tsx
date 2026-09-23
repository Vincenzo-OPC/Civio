interface BrandNameProps {
    className?: string;
}

export default function BrandName({ className = '' }: BrandNameProps) {
    return <span className={className}>CIVIO</span>;
}
