'use client';

import { useEffect, ReactNode, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

interface ProtectedRouteProps {
  children: ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const [checking, setChecking] = useState(true);
  
  useEffect(() => {
    // Só verificar após o carregamento inicial do contexto de autenticação
    if (!loading) {
      if (!isAuthenticated) {
        router.push('/');
      }
      setChecking(false);
    }
  }, [isAuthenticated, router, loading]);
  
  // Mostrar um indicador de carregamento enquanto verifica
  if (checking || loading) {
    return <div className="flex justify-center items-center min-h-screen">Verificando autenticação...</div>;
  }
  
  // Se não estiver autenticado, não renderizar nada (o redirecionamento já foi iniciado)
  if (!isAuthenticated) {
    return null;
  }
  
  // Se estiver autenticado, renderizar o conteúdo protegido
  return <>{children}</>;
}
