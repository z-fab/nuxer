// Tipos para usuário
export interface User {
  id: number;
  nome: string;
  apelido: string;
  email: string | null;
  slack_id: string | null;
  notion_id: string | null;
  notion_user_id: string | null;
}

export interface Wallet {
  wallet_id: string;
  balance: number;
  user: User | null;
}

// Tipos para autenticação
export interface AuthToken {
  access_token: string;
  token_type: string;
}
