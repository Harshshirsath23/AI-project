import { Outlet } from "react-router-dom"
import { motion } from "framer-motion"
import { Zap } from "lucide-react"

export function AuthLayout() {
  return (
    <div className="min-h-screen flex">
      {/* Left panel — branding */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
        {/* Gradient background */}
        <div className="absolute inset-0 gradient-primary" />

        {/* Animated mesh shapes */}
        <motion.div
          className="absolute top-1/4 -left-20 w-96 h-96 rounded-full bg-white/10 blur-3xl"
          animate={{ x: [0, 40, 0], y: [0, -30, 0] }}
          transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute bottom-1/4 right-10 w-80 h-80 rounded-full bg-white/10 blur-3xl"
          animate={{ x: [0, -30, 0], y: [0, 40, 0] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute top-1/2 left-1/3 w-64 h-64 rounded-full bg-white/5 blur-2xl"
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        />

        {/* Content */}
        <div className="relative z-10 flex flex-col justify-between p-12 text-white w-full">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-white/20 backdrop-blur-sm">
              <Zap className="h-5 w-5" />
            </div>
            <span className="text-xl font-bold tracking-tight">Voxera</span>
          </div>

          {/* Hero text */}
          <div className="space-y-6 max-w-lg">
            <motion.h1
              className="text-4xl lg:text-5xl font-bold leading-tight"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
            >
              Intelligent Voice AI
              <br />
              <span className="text-white/80">at Enterprise Scale</span>
            </motion.h1>
            <motion.p
              className="text-lg text-white/70 leading-relaxed"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.6 }}
            >
              Deploy AI voice agents that handle thousands of conversations simultaneously.
              Build, train, and scale your outbound calling campaigns with unmatched precision.
            </motion.p>
          </div>

          {/* Stats */}
          <motion.div
            className="flex gap-12"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.6 }}
          >
            {[
              { value: "99.9%", label: "Uptime" },
              { value: "50ms", label: "Avg Latency" },
              { value: "10M+", label: "Calls Processed" },
            ].map((stat) => (
              <div key={stat.label}>
                <p className="text-2xl font-bold">{stat.value}</p>
                <p className="text-sm text-white/60">{stat.label}</p>
              </div>
            ))}
          </motion.div>
        </div>
      </div>

      {/* Right panel — form */}
      <div className="flex-1 flex items-center justify-center p-6 lg:p-12 bg-background">
        <motion.div
          className="w-full max-w-[420px]"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        >
          <Outlet />
        </motion.div>
      </div>
    </div>
  )
}
