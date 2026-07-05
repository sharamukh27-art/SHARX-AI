/**
 * Chat Page
 */

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { apiClient } from '@/services/api'
import { useChatStore } from '@/context/store'
import type { Message } from '@/types'
import './Chat.css'

const ChatPage: React.FC = () => {
  const [inputValue, setInputValue] = useState('')
  const { currentConversation, messages, addMessage, isLoading, setLoading } = useChatStore()

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      role: 'user',
      content: inputValue,
    }

    addMessage(userMessage)
    setInputValue('')
    setLoading(true)

    try {
      const response = await apiClient.chat([...messages, userMessage], currentConversation?.id)
      addMessage(response.message)
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-page">
      <div className="chat-container">
        <div className="messages-section">
          {messages.map((msg, idx) => (
            <motion.div
              key={idx}
              className={`message ${msg.role}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="message-content">{msg.content}</div>
            </motion.div>
          ))}
          {isLoading && (
            <motion.div className="message assistant" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <div className="message-content">
                <span className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </span>
              </div>
            </motion.div>
          )}
        </div>

        <div className="input-section">
          <div className="input-wrapper">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask me anything..."
              disabled={isLoading}
              className="message-input"
            />
            <button onClick={handleSendMessage} disabled={isLoading} className="send-button">
              {isLoading ? '...' : '→'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatPage
