import { cn } from "@/lib/utils"

interface StatusIndicatorProps {
  status: "active" | "inactive" | "warning" | "error" | "pending"
  label?: string
  pulse?: boolean
  className?: string
}

const statusStyles: Record<StatusIndicatorProps["status"], string> = {
  active: "bg-green-500",
  inactive: "bg-gray-400",
  warning: "bg-amber-500",
  error: "bg-red-500",
  pending: "bg-blue-500",
}

const statusLabels: Record<StatusIndicatorProps["status"], string> = {
  active: "Active",
  inactive: "Inactive",
  warning: "Warning",
  error: "Error",
  pending: "Pending",
}

export function StatusIndicator({
  status,
  label,
  pulse = false,
  className,
}: StatusIndicatorProps) {
  return (
    <div className={cn("flex items-center gap-2", className)}>
      <span className="relative flex h-2.5 w-2.5">
        {pulse && (
          <span
            className={cn(
              "animate-ping absolute inline-flex h-full w-full rounded-full opacity-75",
              statusStyles[status]
            )}
          />
        )}
        <span
          className={cn(
            "relative inline-flex rounded-full h-2.5 w-2.5",
            statusStyles[status]
          )}
        />
      </span>
      {(label || statusLabels[status]) && (
        <span className="text-sm text-muted-foreground">
          {label || statusLabels[status]}
        </span>
      )}
    </div>
  )
}
