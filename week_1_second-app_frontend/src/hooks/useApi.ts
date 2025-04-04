import { useQuery, useMutation, useQueryClient } from 'react-query'

interface UseApiOptions<T> {
  queryKey: string | string[]
  queryFn: () => Promise<T>
  onSuccess?: (data: T) => void
  onError?: (error: Error) => void
  enabled?: boolean
}

interface UseMutationOptions<T, U> {
  mutationFn: (data: U) => Promise<T>
  onSuccess?: (data: T) => void
  onError?: (error: Error) => void
  invalidateQueries?: string[]
}

export function useApi<T>({
  queryKey,
  queryFn,
  onSuccess,
  onError,
  enabled = true,
}: UseApiOptions<T>) {
  return useQuery({
    queryKey,
    queryFn,
    onSuccess,
    onError,
    enabled,
  })
}

export function useApiMutation<T, U = unknown>({
  mutationFn,
  onSuccess,
  onError,
  invalidateQueries = [],
}: UseMutationOptions<T, U>) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn,
    onSuccess: (data) => {
      // Invalidate queries if needed
      invalidateQueries.forEach((queryKey) => {
        queryClient.invalidateQueries(queryKey)
      })
      onSuccess?.(data)
    },
    onError,
  })
}

// Example usage:
/*
const { data: words, isLoading } = useApi({
  queryKey: 'words',
  queryFn: wordService.getWords,
})

const { mutate: createWord } = useApiMutation({
  mutationFn: wordService.createWord,
  invalidateQueries: ['words'],
  onSuccess: () => {
    // Handle success
  },
})
*/
