/**
 * API and domain types for SHAR-X AI
 */

export interface Message {
  role: 'user' | 'assistant' | 'system'
  content: string
}

export interface ChatResponse {
  conversation_id: string
  message: Message
  model: string
}

export interface Conversation {
  id: string
  title: string
  created_at: string
  updated_at: string
}

export interface Note {
  id: string
  title: string
  content: string
  tags: string[]
  created_at: string
  updated_at: string
}

export interface SystemStats {
  cpu_percent: number
  memory: {
    total: number
    available: number
    percent: number
    used: number
  }
  disk: {
    total: number
    used: number
    free: number
    percent: number
  }
}

export interface HealthCheck {
  status: 'healthy' | 'degraded'
  provider: string
  provider_available: boolean
}

export interface AppInfo {
  app_name: string
  version: string
  ai_provider: string
  description: string
}
