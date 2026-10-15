export default function AppLogo() {
    return (
        <span className="inline-flex items-center">
            <img
                src="/images/civio-wordmark.png"
                alt="Civio"
                width={960}
                height={427}
                className="h-9 w-auto group-data-[collapsible=icon]:hidden"
            />
            <img
                src="/images/civio-icon.png"
                alt=""
                width={1024}
                height={562}
                className="hidden size-8 object-contain group-data-[collapsible=icon]:block"
            />
        </span>
    );
}
