import * as React from "react"

type Theme = "light" | "dark" | "system"

interface ThemeProviderState {
  theme: Theme
  setTheme: (theme: Theme) => void
  resolvedTheme: "light" | "dark"
}

const ThemeProviderContext = React.createContext<ThemeProviderState | undefined>(undefined)

interface ThemeProviderProps {
  children: React.ReactNode
  defaultTheme?: Theme
  storageKey?: string
}

export function ThemeProvider({
  children,
  defaultTheme = "system",
  storageKey = "voxera-ui-theme",
}: ThemeProviderProps) {
  const [theme, setThemeState] = React.useState<Theme>(() => {
    if (typeof window === "undefined") return defaultTheme
    return (localStorage.getItem(storageKey) as Theme) || defaultTheme
  })

  const resolvedTheme = React.useMemo(() => {
    if (theme === "system") {
      if (typeof window === "undefined") return "light"
      return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
    }
    return theme
  }, [theme])

  React.useEffect(() => {
    const root = window.document.documentElement
    root.classList.remove("light", "dark")
    root.classList.add(resolvedTheme)
  }, [resolvedTheme])

  React.useEffect(() => {
    if (theme !== "system") return
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)")
    const handleChange = () => {
      const root = window.document.documentElement
      root.classList.remove("light", "dark")
      root.classList.add(mediaQuery.matches ? "dark" : "light")
    }
    mediaQuery.addEventListener("change", handleChange)
    return () => mediaQuery.removeEventListener("change", handleChange)
  }, [theme])

  const setTheme = React.useCallback(
    (newTheme: Theme) => {
      localStorage.setItem(storageKey, newTheme)
      setThemeState(newTheme)
    },
    [storageKey]
  )

  return (
    <ThemeProviderContext.Provider value={{ theme, setTheme, resolvedTheme }}>
      {children}
    </ThemeProviderContext.Provider>
  )
}

export function useTheme() {
  const context = React.useContext(ThemeProviderContext)
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider")
  }
  return context
}
