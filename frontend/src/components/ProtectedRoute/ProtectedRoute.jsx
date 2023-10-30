// 'use client'
// import { useRouter } from 'next/navigation';
// import { jwtDecode } from 'jwt-decode';
// import { useContext } from 'react';

// // import { useCookie } from '../../hooks/useCookie';
// import { useNotification } from '../../hooks/useNotification';
// import { NextColor } from '../../consts/NextColor';
// import { UserIdContext } from '../../contexts/UserIdContext';

// export default function ProtectedRoute({ children, cookie }) {
//   const router = useRouter();
//   const notification = useNotification();
//   const jwt = jwtDecode(cookie);
//   const { setUserId } = useContext(UserIdContext);

//   if (jwt && jwt?.exp > Date.now() / 1000) {
//     return <>{children}</>
//   } else {
//     router.replace('/login');
//     setUserId('');
//     notification.make(NextColor.WARNING, 'Session expired', 'Please log in.');
//     return null;
//   }
// }
