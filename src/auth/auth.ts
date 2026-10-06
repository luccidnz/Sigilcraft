import { useEffect, useState } from 'react';

export interface AuthSession {
  user: { name: string } | null;
  signedIn: boolean;
}

export function useAuth() {
  const [session, setSession] = useState<AuthSession | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem('sigilcraft_session');
    if (stored) {
      try {
        setSession(JSON.parse(stored));
      } catch {
        localStorage.removeItem('sigilcraft_session');
      }
    }
    setLoading(false);
  }, []);

  const signIn = (name: string) => {
    const session: AuthSession = { user: { name }, signedIn: true };
    localStorage.setItem('sigilcraft_session', JSON.stringify(session));
    setSession(session);
  };

  const signOut = () => {
    localStorage.removeItem('sigilcraft_session');
    setSession(null);
  };

  return {
    session,
    loading,
    signIn,
    signOut
  };
}
