'use client'

import { NextUIProvider } from '@nextui-org/react';
import { NotificationProvider } from '../contexts/NotificationContext';
import { UserIdProvider } from '../contexts/UserIdContext';

export default function Providers({ children }) {
  return (
    <NextUIProvider>
      <NotificationProvider>
      <UserIdProvider>
        {children}
        </UserIdProvider>
      </NotificationProvider>
    </NextUIProvider>
  )
}