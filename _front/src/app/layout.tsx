import { AuthProvider } from '@/contexts/AuthContext';
import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'FabBank',
  description: 'Sistema de gerenciamento do FabBank',
};

/**
 * Layout raiz da aplicação
 * 
 * Envolve toda a aplicação com o provedor de autenticação
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
