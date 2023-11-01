import ProtectedRoute from '../../components/ProtectedRoute/ProtectedRoute'

export const metadata = {
  title: 'TagMedX - Groups',
  description: 'TagMedX is an open-source web app built with FastAPI, Next.js, and MySQL, designed for medical image tagging.'
}

export default function GroupsLayout({ children }) {
  return (
    <ProtectedRoute>
      {children}
    </ProtectedRoute>
  )
}