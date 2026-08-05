import { useTheme } from "@/providers/theme-provider"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Bell,
  Search,
  Sun,
  Moon,
  Monitor,
  User,
  Settings,
  LogOut,
  Building2,
} from "lucide-react"
import { cn } from "@/lib/utils"

interface TopNavProps {
  onSearchOpen: () => void
  className?: string
}

export function TopNav({ onSearchOpen, className }: TopNavProps) {
  const { theme, setTheme } = useTheme()

  return (
    <header
      className={cn(
        "sticky top-0 z-30 flex h-16 items-center justify-between gap-4 border-b bg-background/80 backdrop-blur-lg px-6",
        className
      )}
    >
      {/* Left side — search trigger */}
      <button
        onClick={onSearchOpen}
        className="flex items-center gap-2 h-9 px-3 rounded-lg border bg-muted/50 text-sm text-muted-foreground hover:bg-muted transition-colors min-w-[240px]"
      >
        <Search className="h-4 w-4" />
        <span>Search everything...</span>
        <kbd className="ml-auto pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-background px-1.5 text-[10px] font-medium text-muted-foreground">
          ⌘K
        </kbd>
      </button>

      {/* Right side */}
      <div className="flex items-center gap-2">
        {/* Theme toggle */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" className="h-9 w-9">
              {theme === "light" && <Sun className="h-4 w-4" />}
              {theme === "dark" && <Moon className="h-4 w-4" />}
              {theme === "system" && <Monitor className="h-4 w-4" />}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => setTheme("light")}>
              <Sun className="mr-2 h-4 w-4" /> Light
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => setTheme("dark")}>
              <Moon className="mr-2 h-4 w-4" /> Dark
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => setTheme("system")}>
              <Monitor className="mr-2 h-4 w-4" /> System
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        {/* Notifications */}
        <Button variant="ghost" size="icon" className="h-9 w-9 relative">
          <Bell className="h-4 w-4" />
          <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-destructive" />
        </Button>

        {/* User menu */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-9 gap-2 pl-2 pr-3">
              <Avatar className="h-7 w-7">
                <AvatarFallback className="text-xs">HS</AvatarFallback>
              </Avatar>
              <span className="text-sm font-medium hidden sm:inline-block">Harsh S.</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel className="font-normal">
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium">Harsh Shirsath</p>
                <p className="text-xs text-muted-foreground">harsh@voxera.ai</p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <DropdownMenuItem>
                <User className="mr-2 h-4 w-4" /> Profile
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Building2 className="mr-2 h-4 w-4" /> Organization
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Settings className="mr-2 h-4 w-4" /> Settings
              </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="text-destructive focus:text-destructive">
              <LogOut className="mr-2 h-4 w-4" /> Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  )
}
