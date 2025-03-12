import { AppSidebar } from '@/components/app-sidebar';
import ProtectedRoute from '@/components/ProtectedRoute';
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'FabBank',
  description: 'Sistema de gerenciamento do FabBank',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {

    
  return (
  <ProtectedRoute>
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        {children}
      </SidebarInset>
    </SidebarProvider>
  </ProtectedRoute>
);
}
