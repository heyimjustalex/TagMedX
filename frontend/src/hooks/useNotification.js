import { useContext } from 'react'
import { NotificationContext } from '../contexts/NotificationContext'

function useNotification() {
  const notification = useContext(NotificationContext);
  return notification;
}

export { useNotification }