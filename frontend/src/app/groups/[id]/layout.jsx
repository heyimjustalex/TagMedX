import ProtectedRoute from '../../../components/ProtectedRoute/ProtectedRoute'

export const metadata = {
  title: 'TagMedX - Group',
  description: 'TagMedX is an open-source web app built with FastAPI, Next.js, and MySQL, designed for medical image tagging.'
}

export default function GroupLayout({ children }) {
  return (
    <ProtectedRoute>
      {children}
    </ProtectedRoute>
  )
}