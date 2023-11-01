import { useContext } from 'react';

import { UserIdContext } from '../contexts/UserIdContext';

export function useUserId() {
  return useContext(UserIdContext);
}