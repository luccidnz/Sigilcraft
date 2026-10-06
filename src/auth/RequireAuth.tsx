import { useLocation, Navigate } from 'react-router-dom';
import { useAuth, AuthSession } from './auth';

interface RequireAuthProps {
  children: React.ReactNode;
  returnTo?: string;
}

export function RequireAuth({ children, returnTo = '/' }: RequireAuthProps) {
  const { session, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return null;
  }

  if (!session?.signedIn) {
    return <Navigate to={`/auth?returnTo=${encodeURIComponent(location.pathname || returnTo)}`} replace />;
  }

  return <>{children}</>;
}
