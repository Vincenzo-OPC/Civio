interface BrandNameProps {
    className?: string;
}

export default function BrandName({ className = '' }: BrandNameProps) {
    return (
        <span className={className}>
            Civio <span className="font-black text-primary">Review</span>
        </span>
    );
}
