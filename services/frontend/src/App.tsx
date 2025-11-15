import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import WorkspacePage from './pages/WorkspacePage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/workspace/default" replace />} />
        <Route path="/workspace/:workspaceId/*" element={<WorkspacePage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
