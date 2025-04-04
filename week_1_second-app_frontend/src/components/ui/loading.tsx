import React from 'react'
import { Loader2 } from 'lucide-react'

interface LoadingProps {
  size?: number
  className?: string
  text?: string
}

export function Loading({ size = 24, className = '', text }: LoadingProps) {
  return (
    <div className={`flex items-center justify-center space-x-2 ${className}`}>
      <Loader2 className="animate-spin" size={size} />
      {text && <span className="text-muted-foreground">{text}</span>}
    </div>
  )
}

export function PageLoading() {
  return (
    <div className="flex min-h-[400px] items-center justify-center">
      <Loading size={32} text="Loading..." />
    </div>
  )
}

export function TableLoading() {
  return (
    <div className="flex min-h-[200px] items-center justify-center">
      <Loading size={24} text="Loading data..." />
    </div>
  )
}

export function ButtonLoading() {
  return <Loading size={16} />
}
