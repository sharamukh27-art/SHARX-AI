/// <reference types="vite/client" />
/**
 * API client for SHAR-X AI backend
 */

import axios, { AxiosInstance } from 'axios'
import type {
  Message,
  ChatResponse,
  Conversation,
  Note,
  SystemStats,
  HealthCheck,
  AppInfo,
} from '@/types'

class APIClient {
  private client: AxiosInstance

  constructor(baseURL: string = import.meta.env.VITE_API_URL || 'http://localhost:8000') {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }

  // Chat endpoints
  async chat(messages: Message[], conversationId?: string): Promise<ChatResponse> {
    const response = await this.client.post('/api/chat/', {
      messages,
      conversation_id: conversationId,
    })
    return response.data
  }

  async getConversations(): Promise<Conversation[]> {
    const response = await this.client.get('/api/chat/conversations')
    return response.data
  }

  async getConversation(id: string): Promise<{
    conversation: Conversation
    messages: Message[]
  }> {
    const response = await this.client.get(`/api/chat/conversations/${id}`)
    return response.data
  }

  // System endpoints
  async getHealth(): Promise<HealthCheck> {
    const response = await this.client.get('/api/system/health')
    return response.data
  }

  async getSystemStats(): Promise<SystemStats> {
    const response = await this.client.get('/api/system/stats')
    return response.data
  }

  async getAppInfo(): Promise<AppInfo> {
    const response = await this.client.get('/api/system/info')
    return response.data
  }

  // Notes endpoints
  async createNote(title: string, content: string, tags: string[] = []): Promise<Note> {
    const response = await this.client.post('/api/notes/', {
      title,
      content,
      tags,
    })
    return response.data
  }

  async getNotes(): Promise<Note[]> {
    const response = await this.client.get('/api/notes/')
    return response.data
  }

  async getNote(id: string): Promise<Note> {
    const response = await this.client.get(`/api/notes/${id}`)
    return response.data
  }

  async updateNote(id: string, title?: string, content?: string, tags?: string[]): Promise<Note> {
    const response = await this.client.put(`/api/notes/${id}`, {
      title,
      content,
      tags,
    })
    return response.data
  }

  async deleteNote(id: string): Promise<void> {
    await this.client.delete(`/api/notes/${id}`)
  }

  // Memory endpoints
  async addMemory(content: string, category: string = 'general'): Promise<{ id: string }> {
    const response = await this.client.post('/api/memory/add', {
      content,
      category,
    })
    return response.data
  }

  async queryMemory(query: string, nResults: number = 5): Promise<any> {
    const response = await this.client.post('/api/memory/query', {
      query,
      n_results: nResults,
    })
    return response.data
  }

  async getAllMemory(): Promise<any> {
    const response = await this.client.get('/api/memory/all')
    return response.data
  }
}

export const apiClient = new APIClient()
