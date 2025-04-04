import React from 'react'
import { LucideIcon } from 'lucide-react'

interface EmptyStateProps {
  icon?: LucideIcon
  title: string
  description: string
  action?: React.ReactNode
  className?: string
}

export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  className = '',
}: EmptyStateProps) {
  return (
    <div
      className={`flex min-h-[400px] flex-col items-center justify-center rounded-lg border border-dashed p-8 text-center ${className}`}
    >
      {Icon && <Icon className="mb-4 h-12 w-12 text-muted-foreground" />}
      <h3 className="mb-2 text-2xl font-semibold">{title}</h3>
      <p className="mb-4 text-sm text-muted-foreground">{description}</p>
      {action}
    </div>
  )
}

export function TableEmptyState({
  icon: Icon,
  title,
  description,
  action,
  className = '',
}: EmptyStateProps) {
  return (
    <div
      className={`flex min-h-[200px] flex-col items-center justify-center p-4 text-center ${className}`}
    >
      {Icon && <Icon className="mb-2 h-8 w-8 text-muted-foreground" />}
      <h3 className="mb-1 text-lg font-semibold">{title}</h3>
      <p className="mb-4 text-sm text-muted-foreground">{description}</p>
      {action}
    </div>
  )
}
