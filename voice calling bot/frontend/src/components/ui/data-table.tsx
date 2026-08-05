import * as React from "react"
import { cn } from "@/lib/utils"
import { Checkbox } from "@/components/ui/checkbox"
import { Skeleton } from "@/components/ui/skeleton"
import { EmptyState } from "@/components/ui/empty-state"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight, Database } from "lucide-react"
import { motion } from "framer-motion"

export interface Column<T> {
  key: string
  header: string
  cell: (row: T) => React.ReactNode
  className?: string
  sortable?: boolean
}

interface DataTableProps<T> {
  columns: Column<T>[]
  data: T[]
  loading?: boolean
  selectable?: boolean
  selectedRows?: Set<string>
  onSelectionChange?: (selected: Set<string>) => void
  getRowId?: (row: T, index?: number) => string
  emptyTitle?: string
  emptyDescription?: string
  page?: number
  pageSize?: number
  totalCount?: number
  onPageChange?: (page: number) => void
  className?: string
}

export function DataTable<T>({
  columns,
  data,
  loading = false,
  selectable = false,
  selectedRows = new Set(),
  onSelectionChange,
  getRowId = (_row: T, index?: number) => String(index),
  emptyTitle = "No results found",
  emptyDescription = "Try adjusting your search or filters.",
  page = 1,
  pageSize = 10,
  totalCount,
  onPageChange,
  className,
}: DataTableProps<T>) {
  const totalPages = totalCount ? Math.ceil(totalCount / pageSize) : 1

  const handleSelectAll = (checked: boolean) => {
    if (!onSelectionChange) return
    if (checked) {
      const all = new Set(data.map((row, i) => getRowId(row, i)))
      onSelectionChange(all)
    } else {
      onSelectionChange(new Set())
    }
  }

  const handleSelectRow = (id: string, checked: boolean) => {
    if (!onSelectionChange) return
    const next = new Set(selectedRows)
    if (checked) {
      next.add(id)
    } else {
      next.delete(id)
    }
    onSelectionChange(next)
  }

  if (loading) {
    return (
      <div className={cn("rounded-xl border bg-card", className)}>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                {selectable && <th className="p-4 w-[50px]"><Skeleton className="h-4 w-4" /></th>}
                {columns.map((col) => (
                  <th key={col.key} className="p-4 text-left">
                    <Skeleton className="h-4 w-24" />
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: 5 }).map((_, i) => (
                <tr key={i} className="border-b last:border-0">
                  {selectable && <td className="p-4"><Skeleton className="h-4 w-4" /></td>}
                  {columns.map((col) => (
                    <td key={col.key} className="p-4">
                      <Skeleton className="h-4 w-full max-w-[200px]" />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    )
  }

  if (data.length === 0) {
    return (
      <div className={cn("rounded-xl border bg-card", className)}>
        <EmptyState
          icon={Database}
          title={emptyTitle}
          description={emptyDescription}
        />
      </div>
    )
  }

  return (
    <div className={cn("rounded-xl border bg-card", className)}>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b bg-muted/30">
              {selectable && (
                <th className="p-4 w-[50px]">
                  <Checkbox
                    checked={data.length > 0 && selectedRows.size === data.length}
                    onCheckedChange={(checked) => handleSelectAll(!!checked)}
                  />
                </th>
              )}
              {columns.map((col) => (
                <th
                  key={col.key}
                  className={cn(
                    "p-4 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider",
                    col.className
                  )}
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => {
              const rowId = getRowId(row, index)
              const isSelected = selectedRows.has(rowId)
              return (
                <motion.tr
                  key={rowId}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: index * 0.03 }}
                  className={cn(
                    "border-b last:border-0 transition-colors hover:bg-muted/50",
                    isSelected && "bg-primary/5"
                  )}
                >
                  {selectable && (
                    <td className="p-4">
                      <Checkbox
                        checked={isSelected}
                        onCheckedChange={(checked) => handleSelectRow(rowId, !!checked)}
                      />
                    </td>
                  )}
                  {columns.map((col) => (
                    <td key={col.key} className={cn("p-4 text-sm", col.className)}>
                      {col.cell(row)}
                    </td>
                  ))}
                </motion.tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {onPageChange && totalCount !== undefined && totalPages > 1 && (
        <div className="flex items-center justify-between px-4 py-3 border-t">
          <p className="text-sm text-muted-foreground">
            Showing {((page - 1) * pageSize) + 1}–{Math.min(page * pageSize, totalCount)} of {totalCount}
          </p>
          <div className="flex items-center gap-1">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onPageChange(1)}
              disabled={page <= 1}
            >
              <ChevronsLeft className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onPageChange(page - 1)}
              disabled={page <= 1}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <span className="text-sm px-2">
              {page} / {totalPages}
            </span>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onPageChange(page + 1)}
              disabled={page >= totalPages}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onPageChange(totalPages)}
              disabled={page >= totalPages}
            >
              <ChevronsRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
