import * as React from "react";

const MOBILE_BREAKPOINT = 768;

/**
 * Custom hook to determine if the screen size is mobile.
 * Uses `window.matchMedia` and `resize` event for better reactivity.
 */
export function useIsMobile(): boolean {
  const [isMobile, setIsMobile] = React.useState<boolean>(
    () => window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`).matches
  );

  React.useEffect(() => {
    const updateSize = () => setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
    const mediaQuery = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`);

    // Initial check
    updateSize();

    // Add listeners
    mediaQuery.addEventListener("change", updateSize);
    window.addEventListener("resize", updateSize);

    return () => {
      mediaQuery.removeEventListener("change", updateSize);
      window.removeEventListener("resize", updateSize);
    };
  }, []);

  return isMobile;
}
