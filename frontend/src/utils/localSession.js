import { jwtDecode } from 'jwt-decode';
import { getCookie } from './cookie';

export function checkSession() {
  const token = getCookie('token')
  const jwt = token ? jwtDecode(token) : null;
  return jwt && jwt?.exp > Date.now() / 1000 ? jwt?.id : false;
}