import { jwtDecode } from 'jwt-decode';
import { cookies } from 'next/headers'

export function checkSession() {
  const cookieStore = cookies();
  const token = cookieStore.get('token');
  const jwt = token ? jwtDecode(token.value) : null;
  return jwt && jwt?.exp > Date.now() / 1000 ? jwt?.id : false;
}