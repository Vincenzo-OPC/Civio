import { SelectField } from '@/components/ui/select';
import { AI_MODEL_OPTIONS } from '@/constants/ai-models';

interface AiModelSelectProps {
    value: string;
    onValueChange: (value: string) => void;
    disabled?: boolean;
    className?: string;
}

export function AiModelSelect({
    value,
    onValueChange,
    disabled = false,
    className,
}: AiModelSelectProps) {
    return (
        <SelectField
            value={value}
            disabled={disabled}
            onValueChange={onValueChange}
            options={AI_MODEL_OPTIONS.map((opt) => ({
                value: opt.value,
                label: opt.label,
            }))}
            className={className}
        />
    );
}
