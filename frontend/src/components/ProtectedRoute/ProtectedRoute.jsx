'use client'
import { useRouter } from 'next/navigation';
import { jwtDecode } from 'jwt-decode';

import { useNotification } from '../../hooks/useNotification';
import { NextColor } from '../../consts/NextColor';
import { getCookie } from '../../utils/cookie';

export default function ProtectedRoute({ children }) {
  const router = useRouter();
  const notification = useNotification();
  const cookie = getCookie('token');
  const jwt = cookie ? jwtDecode(cookie) : null;

  if (jwt && jwt?.exp > Date.now() / 1000) {
    return <>{children}</>
  } else {
    notification.make(NextColor.WARNING, 'Session expired', 'Please log in.');
    router.replace('/login');
    return null;
  }
}
