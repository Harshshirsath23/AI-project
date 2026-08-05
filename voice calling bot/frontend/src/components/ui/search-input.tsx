import * as React from "react"
import { Search, X } from "lucide-react"
import { cn } from "@/lib/utils"

interface SearchInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "onChange"> {
  value: string
  onChange: (value: string) => void
  shortcutHint?: string
  className?: string
}

export function SearchInput({
  value,
  onChange,
  shortcutHint = "⌘K",
  placeholder = "Search...",
  className,
  ...props
}: SearchInputProps) {
  const inputRef = React.useRef<HTMLInputElement>(null)

  return (
    <div className={cn("relative flex items-center", className)}>
      <Search className="absolute left-3 h-4 w-4 text-muted-foreground pointer-events-none" />
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="flex h-9 w-full rounded-lg border border-input bg-background pl-9 pr-20 py-2 text-sm shadow-sm transition-all duration-200 placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-1"
        {...props}
      />
      <div className="absolute right-2 flex items-center gap-1">
        {value && (
          <button
            onClick={() => {
              onChange("")
              inputRef.current?.focus()
            }}
            className="rounded-md p-1 hover:bg-muted transition-colors"
          >
            <X className="h-3.5 w-3.5 text-muted-foreground" />
          </button>
        )}
        {shortcutHint && !value && (
          <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 text-[10px] font-medium text-muted-foreground">
            {shortcutHint}
          </kbd>
        )}
      </div>
    </div>
  )
}
