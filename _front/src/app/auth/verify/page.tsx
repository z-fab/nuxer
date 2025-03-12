'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { authService } from '@/lib/api';

/**
 * Página de verificação do magic link
 * 
 * Verifica o token do magic link e obtém um token JWT
 */
export default function VerifyLogin() {
  const [verifying, setVerifying] = useState<boolean>(true);
  const [error, setError] = useState<string>('');
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login } = useAuth();
  
  useEffect(() => {
    const verifyToken = async (): Promise<void> => {
      const token = searchParams.get('token');
      
      if (!token) {
        setError('Link inválido. Por favor, solicite um novo link de login.');
        setVerifying(false);
        return;
      }
      
      try {
        const data = await authService.verifyMagicLink(token);
        // Login bem-sucedido
        login(data.access_token);
        
        // Redirecionar para o dashboard
        router.push('/house');
      } catch (err) {
        setError('O link expirou ou é inválido. Por favor, solicite um novo link de login.');
        setVerifying(false);
      }
    };
    
    verifyToken();
  }, [searchParams, login, router]);
  
  return (
    <main className="flex flex-col justify-center items-center p-5 min-h-screen">
      <h1 className="text-4xl font-bold text-center mb-8">Verificando seu login</h1>
      
      {verifying ? (
        <p>Aguarde enquanto verificamos seu link de login...</p>
      ) : (
        <div className="text-error text-center">
          <p>{error}</p>
          <button 
            onClick={() => router.push('/')} 
            className="mt-4 px-6 py-3 bg-primary text-white border-none rounded-md text-base hover:bg-primary-dark"
          >
            Voltar para o login
          </button>
        </div>
      )}
    </main>
  );
}
