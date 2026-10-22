import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';

interface ExamErrorDialogProps {
    message: string;
    onDismiss: () => void;
}

// Loaded only when an error occurs, so it stays out of the exam page chunk.
export function ExamErrorDialog({ message, onDismiss }: ExamErrorDialogProps) {
    return (
        <Dialog open onOpenChange={(open) => !open && onDismiss()}>
            <DialogContent className="sm:max-w-2xl">
                <DialogHeader>
                    <DialogTitle className="text-red-600">Error</DialogTitle>
                    <p className="mt-2 text-base leading-relaxed text-slate-600">
                        {message}
                    </p>
                </DialogHeader>
                <DialogFooter>
                    <Button
                        onClick={onDismiss}
                        className="bg-red-600 text-white hover:bg-red-700"
                    >
                        Dismiss
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
