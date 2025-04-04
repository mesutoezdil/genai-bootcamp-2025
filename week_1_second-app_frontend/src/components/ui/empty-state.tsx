import React from 'react'
import { AlertTriangle, FileQuestion } from 'lucide-react'

interface EmptyStateProps {
  title?: string
  message?: string
  icon?: 'error' | 'empty'
  className?: string
  children?: React.ReactNode
}

export function EmptyState({
  title = 'No results found',
  message = 'Try adjusting your search or filters.',
  icon = 'empty',
  className = '',
  children,
}: EmptyStateProps): JSX.Element {
  const Icon = icon === 'error' ? AlertTriangle : FileQuestion

  return (
    <div
      className={`flex min-h-[200px] flex-col items-center justify-center space-y-4 rounded-lg border border-dashed p-8 text-center ${className}`}
    >
      <Icon className="h-12 w-12 text-muted-foreground" />
      <div>
        <h3 className="mb-1 text-lg font-medium">{title}</h3>
        <p className="text-sm text-muted-foreground">{message}</p>
      </div>
      {children}
    </div>
  )
}

export function ErrorState({
  title = 'Something went wrong',
  message = 'There was an error loading the data. Please try again.',
  className = '',
  children,
}: EmptyStateProps): JSX.Element {
  return (
    <EmptyState
      title={title}
      message={message}
      icon="error"
      className={className}
    >
      {children}
    </EmptyState>
  )
}
