/**
 * Settings Page
 */

import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { apiClient } from '@/services/api'
import { useChatStore } from '@/context/store'
import './Settings.css'

const SettingsPage: React.FC = () => {
  const { appInfo, health } = useChatStore()
  const [stats, setStats] = React.useState<any>(null)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await apiClient.getSystemStats()
        setStats(data)
      } catch (error) {
        console.error('Failed to fetch system stats:', error)
      }
    }

    fetchStats()
    const interval = setInterval(fetchStats, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="settings-page">
      <div className="settings-container">
        <div className="settings-header">
          <h1>Settings & System Info</h1>
        </div>

        <div className="settings-grid">
          {appInfo && (
            <motion.div className="settings-card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <h2>Application</h2>
              <div className="info-item">
                <span className="label">Name:</span>
                <span className="value">{appInfo.app_name}</span>
              </div>
              <div className="info-item">
                <span className="label">Version:</span>
                <span className="value">{appInfo.version}</span>
              </div>
              <div className="info-item">
                <span className="label">Provider:</span>
                <span className="value">{appInfo.ai_provider}</span>
              </div>
            </motion.div>
          )}

          {health && (
            <motion.div className="settings-card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <h2>System Health</h2>
              <div className="info-item">
                <span className="label">Status:</span>
                <span className={`value status-${health.status}`}>{health.status}</span>
              </div>
              <div className="info-item">
                <span className="label">AI Provider Available:</span>
                <span className={`value ${health.provider_available ? 'success' : 'error'}`}>
                  {health.provider_available ? '✓ Yes' : '✗ No'}
                </span>
              </div>
            </motion.div>
          )}

          {stats && (
            <motion.div className="settings-card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <h2>System Resources</h2>
              <div className="info-item">
                <span className="label">CPU Usage:</span>
                <span className="value">{stats.cpu_percent.toFixed(1)}%</span>
              </div>
              <div className="info-item">
                <span className="label">Memory Usage:</span>
                <span className="value">{stats.memory.percent.toFixed(1)}%</span>
              </div>
              <div className="info-item">
                <span className="label">Disk Usage:</span>
                <span className="value">{stats.disk.percent.toFixed(1)}%</span>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  )
}

export default SettingsPage
