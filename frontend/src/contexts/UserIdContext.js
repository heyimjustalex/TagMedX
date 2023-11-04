'use client'
import { createContext, useState } from 'react';

import { checkSession } from '../utils/localSession';

const UserIdContext = createContext();

const UserIdProvider = ({ children }) => {
  const [userId, setUserId] = useState(checkSession());

  return (
    <UserIdContext.Provider value={{ userId, setUserId }}>
      {children}
    </UserIdContext.Provider>
  )
}

export { UserIdProvider, UserIdContext }
