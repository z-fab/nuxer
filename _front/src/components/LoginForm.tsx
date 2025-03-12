import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useState, FormEvent } from 'react';
import { authService } from '@/lib/api';

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"form">) {



  const [email, setEmail] = useState<string>('');
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    setError('');
    
    try {
      await authService.requestMagicLink(email);
      setIsSubmitted(true);
    } catch (err) {
      setError('Ocorreu um erro ao solicitar o link de login. Tente novamente.');
      console.error(err);
    }
  };


  return (
    isSubmitted ? (
      <div className="flex flex-col items-center gap-8 text-center w-full max-w-md mx-auto">
        <p>Se você estiver na lista de convidados para a casa do Nuxer, olhe seu Slack!</p>
        <Button variant="default" onClick={() => setIsSubmitted(false)}>
          Retornar para Login
        </Button>
      </div>
      
    ) : (
    <form onSubmit={handleSubmit} className={cn("flex flex-col gap-6", className)} {...props}>
      <div className="flex flex-col items-center gap-2 text-center">
        <h1 className="text-2xl font-bold">Entre na casa do Nuxer</h1>
        <p className="text-muted-foreground text-sm text-balance">
          Coloque seu email para receber um link mágico no <b>Slack</b>
        </p>
      </div>
      <div className="grid gap-6">
        <div className="grid gap-3">
          <Label htmlFor="email">Email</Label>
          <Input 
            id="email" 
            type="email" 
            placeholder="nome@merkle.com" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required 
          />
          {error && <p className="text-red-500 text-sm">{error}</p>}
        </div>
        <Button type="submit" className="w-full">
          Solicitar Link
        </Button>
      </div>
      <div className="text-center text-sm">
        Não consegue acessar? Fale com o Fabs
      </div>
    </form>)
  )
}
