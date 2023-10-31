'use clinet'
import ProtectedRoute from '../../components/ProtectedRoute/ProtectedRoute'

export default function GroupsLayout({ children }) {
  return (
    <>
      <ProtectedRoute>
      {children}
      </ProtectedRoute>
    </>
  )
}