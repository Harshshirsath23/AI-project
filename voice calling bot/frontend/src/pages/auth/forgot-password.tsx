import * as React from "react"
import { Link } from "react-router-dom"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Mail, ArrowLeft, CheckCircle2 } from "lucide-react"

const forgotSchema = z.object({
  email: z.string().email("Please enter a valid email address"),
})

type ForgotForm = z.infer<typeof forgotSchema>

export function ForgotPasswordPage() {
  const [isLoading, setIsLoading] = React.useState(false)
  const [isSubmitted, setIsSubmitted] = React.useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    getValues,
  } = useForm<ForgotForm>({
    resolver: zodResolver(forgotSchema),
  })

  const onSubmit = async (_data: ForgotForm) => {
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
          <h2 className="text-2xl font-bold tracking-tight">Check your email</h2>
          <p className="text-muted-foreground text-sm">
            We sent a password reset link to<br />
            <span className="font-medium text-foreground">{getValues("email")}</span>
          </p>
        </div>
        <Button variant="outline" className="w-full" asChild>
          <Link to="/login">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to sign in
          </Link>
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
        <h2 className="text-2xl font-bold tracking-tight">Forgot password?</h2>
        <p className="text-muted-foreground text-sm">
          No worries, we&apos;ll send you reset instructions.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="name@company.com"
            icon={<Mail className="h-4 w-4" />}
            error={!!errors.email}
            {...register("email")}
          />
          {errors.email && (
            <p className="text-xs text-destructive">{errors.email.message}</p>
          )}
        </div>

        <Button type="submit" className="w-full h-11" loading={isLoading}>
          Send reset link
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
