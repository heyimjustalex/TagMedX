'use client'

import { NextUIProvider } from '@nextui-org/react';
import { NotificationProvider } from '../contexts/NotificationContext';

export default function Providers({ children }) {
  return (
    <NextUIProvider>
      <NotificationProvider>
        {children}
      </NotificationProvider>
    </NextUIProvider>
  )
}