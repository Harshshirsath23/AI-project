import { useToast } from "@/hooks/use-toast"
import { AnimatePresence, motion } from "framer-motion"
import { X, CheckCircle2, AlertCircle, AlertTriangle, Info } from "lucide-react"
import { cn } from "@/lib/utils"
import type { ToastVariant } from "@/hooks/use-toast"

const variantStyles: Record<ToastVariant, string> = {
  default: "bg-background border",
  success: "bg-green-50 dark:bg-green-950/50 border-green-200 dark:border-green-800",
  destructive: "bg-red-50 dark:bg-red-950/50 border-red-200 dark:border-red-800",
  warning: "bg-amber-50 dark:bg-amber-950/50 border-amber-200 dark:border-amber-800",
  info: "bg-blue-50 dark:bg-blue-950/50 border-blue-200 dark:border-blue-800",
}

const variantIcons: Record<ToastVariant, React.ReactNode> = {
  default: null,
  success: <CheckCircle2 className="h-5 w-5 text-green-600 dark:text-green-400 shrink-0" />,
  destructive: <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 shrink-0" />,
  warning: <AlertTriangle className="h-5 w-5 text-amber-600 dark:text-amber-400 shrink-0" />,
  info: <Info className="h-5 w-5 text-blue-600 dark:text-blue-400 shrink-0" />,
}

export function Toaster() {
  const { toasts, dismiss } = useToast()

  return (
    <div className="fixed bottom-4 right-4 z-[100] flex flex-col gap-2 max-w-[420px] w-full pointer-events-none">
      <AnimatePresence mode="popLayout">
        {toasts.map((t) => {
          const variant = t.variant ?? "default"
          return (
            <motion.div
              key={t.id}
              layout
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 10, scale: 0.95 }}
              transition={{ type: "spring", damping: 25, stiffness: 300 }}
              className={cn(
                "pointer-events-auto flex items-start gap-3 rounded-xl border p-4 shadow-lg",
                variantStyles[variant]
              )}
            >
              {variantIcons[variant]}
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold">{t.title}</p>
                {t.description && (
                  <p className="text-sm text-muted-foreground mt-0.5">{t.description}</p>
                )}
              </div>
              <button
                onClick={() => dismiss(t.id)}
                className="shrink-0 rounded-md p-1 opacity-70 hover:opacity-100 transition-opacity"
              >
                <X className="h-4 w-4" />
              </button>
            </motion.div>
          )
        })}
      </AnimatePresence>
    </div>
  )
}
