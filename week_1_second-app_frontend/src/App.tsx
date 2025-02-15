import { ThemeProvider } from "@/components/theme-provider"
import { BrowserRouter as Router } from "react-router-dom"
import AppSidebar from "@/components/Sidebar"
import Breadcrumbs from "@/components/Breadcrumbs"
import AppRouter from "@/components/AppRouter"
import { NavigationProvider } from "@/context/NavigationContext"

import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"

export default function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <Router>
        <NavigationProvider>
          <SidebarProvider>
            <div className="flex min-h-screen">
              <AppSidebar />
              <SidebarInset>
                <main className="flex-1 p-6">
                  <Breadcrumbs />
                  <AppRouter />
                </main>
              </SidebarInset>
            </div>
          </SidebarProvider>
        </NavigationProvider>
      </Router>
    </ThemeProvider>
  )
}
