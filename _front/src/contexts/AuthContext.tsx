'use client';

import { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { User } from '@/types';
import { authService } from '@/lib/api';

interface AuthContextType {
  token: string | null;
  user: User | null;
  login: (token: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
  loading: boolean; // Novo estado
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  user: null,
  login: () => {},
  logout: () => {},
  isAuthenticated: false,
  loading: true // Valor padrão
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true); // Inicialmente carregando
  const router = useRouter();
  
  // Carregar token do localStorage ao iniciar
  useEffect(() => {
    const initAuth = async () => {
      try {
        const storedToken = localStorage.getItem('token');
        
        if (storedToken) {
          setToken(storedToken);
          try {
            // Tenta obter informações do usuário
            const userData = await authService.getCurrentUser(storedToken);
            setUser(userData);
          } catch (error) {
            console.error('Erro ao buscar informações do usuário:', error);
            // Se falhar, limpa o token (provavelmente inválido)
            localStorage.removeItem('token');
            setToken(null);
          }
        }
      } catch (error) {
        console.error('Erro ao inicializar autenticação:', error);
      } finally {
        // Marca como carregado, independentemente do resultado
        setLoading(false);
      }
    };
    
    initAuth();
  }, []);
  
  const login = (newToken: string): void => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    // Buscar informações do usuário após login
    fetchUserInfo(newToken);
  };
  
  const fetchUserInfo = async (currentToken: string): Promise<void> => {
    try {
      const userData = await authService.getCurrentUser(currentToken);
      setUser(userData);
    } catch (error) {
      console.error('Erro ao buscar informações do usuário:', error);
      logout();
    }
  };
  
  const logout = (): void => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    router.push('/');
  };
  
  return (
    <AuthContext.Provider value={{ 
      token, 
      user, 
      login, 
      logout, 
      isAuthenticated: !!token,
      loading
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
