// 'use clinet'
// import { createContext, useState } from 'react';
// import { jwtDecode } from 'jwt-decode';

// import { useCookie } from '../hooks/useCookie';

// const UserIdContext = createContext();

// const UserIdProvider = ({ children }) => {
//   const cookie = useCookie('token');
//   const jwt = cookie ? jwtDecode(cookie) : null;
//   const [userId, setUserId] = useState(jwt && jwt?.exp > Date.now() / 1000 ? jwt.id : '');

//   return (
//     <UserIdContext.Provider value={{ userId, setUserId }}>
//       {children}
//     </UserIdContext.Provider>
//   )
// }

// export { UserIdProvider, UserIdContext }
