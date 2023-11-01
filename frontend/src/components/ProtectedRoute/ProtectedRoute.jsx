import { redirect } from 'next/navigation'
import { checkSession } from '../../utils/serverSession';

export default function ProtectedRoute({ children }) {
  if (checkSession()) {
    return <>{children}</>
  } else {
    redirect('/login?expired=1')
  }
}
