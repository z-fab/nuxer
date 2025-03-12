export default function Page() {

//   const { token, user, logout } = useAuth();
//   const [wallets, setWallets] = useState<Wallet[]>([]);
//   const [loading, setLoading] = useState<boolean>(false);
//   const [error, setError] = useState<string>('');
  

//   const fetchWallets = async (): Promise<void> => {
//     if (!token) return;
    
//     setLoading(true);
//     setError('');
    
//     try {
//       const data = await fabBankService.getWallets(token);
//       setWallets(data);
//     } catch (err) {
//       setError('Erro ao buscar carteiras. Por favor, tente novamente.');
//       console.error(err);
//     } finally {
//       setLoading(false);
//     }
//   }

    return (
        <div>
        <h1>Fabbank</h1>
        </div>
    );
    }