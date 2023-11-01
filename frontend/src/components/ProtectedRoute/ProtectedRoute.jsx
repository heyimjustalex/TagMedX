import { jwtDecode } from 'jwt-decode';
import { redirect } from 'next/navigation'
import { cookies } from 'next/headers'

export default function ProtectedRoute({ children }) {
  const cookieStore = cookies()
  const cookie = cookieStore.get('token')
  const jwt = cookie ? jwtDecode(cookie) : null;

  if (jwt && jwt?.exp > Date.now() / 1000) {
    return <>{children}</>
  } else {
    redirect('/login?expired=1')
  }
}
