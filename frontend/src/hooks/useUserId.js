import { jwtDecode } from 'jwt-decode';

import { getCookie } from '../utils/cookie';

export function useUserId() {
  const cookie = getCookie('token');
  const jwt = cookie ? jwtDecode(cookie) : null;

  if (jwt && jwt?.exp > Date.now() / 1000) {
    return jwt.sub;
  } else {
    return null;
  }
}