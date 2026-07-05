/**
 * Main App Component
 */

import { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { apiClient } from '@/services/api'
import { useChatStore } from '@/context/store'
import ChatPage from '@/pages/Chat'
import SettingsPage from '@/pages/Settings'
import NotesPage from '@/pages/Notes'
import './App.css'

function App() {
  const { setAppInfo, setHealth } = useChatStore()

  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Fetch app info
        const info = await apiClient.getAppInfo()
        setAppInfo(info)

        // Check health
        const health = await apiClient.getHealth()
        setHealth(health)
      } catch (error) {
        console.error('Failed to initialize app:', error)
      }
    }

    initializeApp()
  }, [setAppInfo, setHealth])

  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/notes" element={<NotesPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
