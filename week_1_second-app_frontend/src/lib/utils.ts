import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combines multiple class names into a single, optimized Tailwind-compatible string.
 * 
 * @param inputs - Class names or conditional class objects
 * @returns A merged and optimized class string
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
