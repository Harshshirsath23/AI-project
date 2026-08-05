import * as React from "react"

// Toast types
export type ToastVariant = "default" | "success" | "destructive" | "warning" | "info"

export interface Toast {
  id: string
  title: string
  description?: string
  variant?: ToastVariant
  duration?: number
}

interface ToastState {
  toasts: Toast[]
}

type ToastAction =
  | { type: "ADD_TOAST"; toast: Toast }
  | { type: "REMOVE_TOAST"; toastId: string }

let count = 0
function genId() {
  count = (count + 1) % Number.MAX_SAFE_INTEGER
  return count.toString()
}

const listeners: Array<(state: ToastState) => void> = []
let memoryState: ToastState = { toasts: [] }

function dispatch(action: ToastAction) {
  switch (action.type) {
    case "ADD_TOAST":
      memoryState = {
        ...memoryState,
        toasts: [action.toast, ...memoryState.toasts].slice(0, 5),
      }
      break
    case "REMOVE_TOAST":
      memoryState = {
        ...memoryState,
        toasts: memoryState.toasts.filter((t) => t.id !== action.toastId),
      }
      break
  }
  listeners.forEach((listener) => listener(memoryState))
}

function toast(props: Omit<Toast, "id">) {
  const id = genId()
  const duration = props.duration ?? 5000

  dispatch({
    type: "ADD_TOAST",
    toast: { ...props, id },
  })

  if (duration > 0) {
    setTimeout(() => {
      dispatch({ type: "REMOVE_TOAST", toastId: id })
    }, duration)
  }

  return id
}

function useToast() {
  const [state, setState] = React.useState<ToastState>(memoryState)

  React.useEffect(() => {
    listeners.push(setState)
    return () => {
      const index = listeners.indexOf(setState)
      if (index > -1) {
        listeners.splice(index, 1)
      }
    }
  }, [])

  return {
    ...state,
    toast,
    dismiss: (toastId: string) =>
      dispatch({ type: "REMOVE_TOAST", toastId }),
  }
}

export { useToast, toast }
