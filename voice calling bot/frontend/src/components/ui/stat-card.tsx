import { motion } from "framer-motion"
import { cn } from "@/lib/utils"
import { TrendingUp, TrendingDown, Minus } from "lucide-react"
import type { LucideIcon } from "lucide-react"
import { GlowingEffect } from "./glowing-effect"

interface StatCardProps {
  title: string
  value: string | number
  change?: number
  changeLabel?: string
  icon?: LucideIcon
  iconColor?: string
  className?: string
  loading?: boolean
}

export function StatCard({
  title,
  value,
  change,
  changeLabel,
  icon: Icon,
  iconColor = "text-primary",
  className,
  loading = false,
}: StatCardProps) {
  if (loading) {
    return (
      <div className={cn("rounded-xl border bg-card p-6", className)}>
        <div className="flex items-center justify-between mb-4">
          <div className="h-4 w-24 bg-muted animate-pulse rounded" />
          <div className="h-10 w-10 bg-muted animate-pulse rounded-xl" />
        </div>
        <div className="h-8 w-20 bg-muted animate-pulse rounded mb-2" />
        <div className="h-3 w-32 bg-muted animate-pulse rounded" />
      </div>
    )
  }

  const trendDirection = change === undefined ? null : change > 0 ? "up" : change < 0 ? "down" : "neutral"

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", damping: 25, stiffness: 300 }}
      className={cn(
        "rounded-xl border bg-card p-6 hover:shadow-md hover:border-primary/20 transition-all duration-200 group",
        className
      )}
    >
      <GlowingEffect
        spread={200}
        glow={true}
        disabled={false}
        borderWidth={2}
        className="opacity-0 group-hover:opacity-100 transition-opacity duration-500"
      />
      
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          {Icon && (
            <div className={cn("p-2.5 rounded-xl bg-primary/10 transition-colors group-hover:bg-primary/15", iconColor)}>
              <Icon className="h-5 w-5" />
            </div>
          )}
        </div>

        <div className="space-y-1">
          <motion.p
            className="text-3xl font-bold tracking-tight"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.1 }}
          >
            {value}
          </motion.p>

          {change !== undefined && (
            <div className="flex items-center gap-1.5">
              <span
                className={cn(
                  "inline-flex items-center gap-0.5 text-xs font-medium px-1.5 py-0.5 rounded-md",
                  trendDirection === "up" && "text-green-700 dark:text-green-400 bg-green-100 dark:bg-green-900/30",
                  trendDirection === "down" && "text-red-700 dark:text-red-400 bg-red-100 dark:bg-red-900/30",
                  trendDirection === "neutral" && "text-muted-foreground bg-muted"
                )}
              >
                {trendDirection === "up" && <TrendingUp className="h-3 w-3" />}
                {trendDirection === "down" && <TrendingDown className="h-3 w-3" />}
                {trendDirection === "neutral" && <Minus className="h-3 w-3" />}
                {change > 0 ? "+" : ""}{change}%
              </span>
              {changeLabel && (
                <span className="text-xs text-muted-foreground">{changeLabel}</span>
              )}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  )
}
