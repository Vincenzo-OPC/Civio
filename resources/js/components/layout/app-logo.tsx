export default function AppLogo() {
    return (
        <span className="inline-flex items-center">
            <img
                src="/images/civio-wordmark-360.png"
                alt="Civio"
                width={360}
                height={120}
                className="h-9 w-auto group-data-[collapsible=icon]:hidden"
            />
            <img
                src="/images/civio-icon-320.png"
                alt=""
                width={320}
                height={176}
                loading="lazy"
                className="hidden size-8 object-contain group-data-[collapsible=icon]:block"
            />
        </span>
    );
}
