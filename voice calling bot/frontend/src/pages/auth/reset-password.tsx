import * as React from "react"
import { Link } from "react-router-dom"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Lock, ArrowLeft, CheckCircle2 } from "lucide-react"
import { cn } from "@/lib/utils"

const resetSchema = z
  .object({
    password: z.string().min(8, "Password must be at least 8 characters"),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"],
  })

type ResetForm = z.infer<typeof resetSchema>

function getPasswordStrength(password: string): { score: number; label: string; color: string } {
  let score = 0
  if (password.length >= 8) score++
  if (password.length >= 12) score++
  if (/[A-Z]/.test(password)) score++
  if (/[0-9]/.test(password)) score++
  if (/[^A-Za-z0-9]/.test(password)) score++

  if (score <= 1) return { score: 1, label: "Weak", color: "bg-red-500" }
  if (score <= 2) return { score: 2, label: "Fair", color: "bg-amber-500" }
  if (score <= 3) return { score: 3, label: "Good", color: "bg-blue-500" }
  if (score <= 4) return { score: 4, label: "Strong", color: "bg-green-500" }
  return { score: 5, label: "Very Strong", color: "bg-green-600" }
}

export function ResetPasswordPage() {
  const [isLoading, setIsLoading] = React.useState(false)
  const [isSubmitted, setIsSubmitted] = React.useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<ResetForm>({
    resolver: zodResolver(resetSchema),
  })

  const password = watch("password", "")
  const strength = password ? getPasswordStrength(password) : null

  const onSubmit = async (_data: ResetForm) => {
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1500))
    setIsLoading(false)
    setIsSubmitted(true)
  }

  if (isSubmitted) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="space-y-6 text-center"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", damping: 15 }}
          className="mx-auto w-16 h-16 rounded-2xl bg-green-100 dark:bg-green-900/30 flex items-center justify-center"
        >
          <CheckCircle2 className="h-8 w-8 text-green-600 dark:text-green-400" />
        </motion.div>
        <div className="space-y-2">
          <h2 className="text-2xl font-bold tracking-tight">Password reset</h2>
          <p className="text-muted-foreground text-sm">
            Your password has been successfully reset.
            <br />You can now sign in with your new password.
          </p>
        </div>
        <Button className="w-full" asChild>
          <Link to="/login">Continue to sign in</Link>
        </Button>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-8"
    >
      <div className="space-y-2">
        <h2 className="text-2xl font-bold tracking-tight">Set new password</h2>
        <p className="text-muted-foreground text-sm">
          Your new password must be different from previously used passwords.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="password">New password</Label>
          <Input
            id="password"
            type="password"
            placeholder="Enter new password"
            icon={<Lock className="h-4 w-4" />}
            error={!!errors.password}
            {...register("password")}
          />
          {strength && (
            <div className="space-y-1.5">
              <div className="flex gap-1">
                {[1, 2, 3, 4, 5].map((level) => (
                  <div
                    key={level}
                    className={cn(
                      "h-1 flex-1 rounded-full transition-all duration-300",
                      level <= strength.score ? strength.color : "bg-muted"
                    )}
                  />
                ))}
              </div>
              <p className="text-xs text-muted-foreground">
                Password strength: <span className="font-medium">{strength.label}</span>
              </p>
            </div>
          )}
          {errors.password && (
            <p className="text-xs text-destructive">{errors.password.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="confirmPassword">Confirm password</Label>
          <Input
            id="confirmPassword"
            type="password"
            placeholder="Confirm new password"
            icon={<Lock className="h-4 w-4" />}
            error={!!errors.confirmPassword}
            {...register("confirmPassword")}
          />
          {errors.confirmPassword && (
            <p className="text-xs text-destructive">{errors.confirmPassword.message}</p>
          )}
        </div>

        <Button type="submit" className="w-full h-11" loading={isLoading}>
          Reset password
        </Button>
      </form>

      <div className="text-center">
        <Link
          to="/login"
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to sign in
        </Link>
      </div>
    </motion.div>
  )
}
