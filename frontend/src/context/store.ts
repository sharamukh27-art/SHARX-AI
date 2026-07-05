/**
 * Global state management with Zustand
 */

import { create } from 'zustand'
import type { Conversation, Message, Note, AppInfo, HealthCheck } from '@/types'

interface ChatStore {
  currentConversation: Conversation | null
  messages: Message[]
  conversations: Conversation[]
  isLoading: boolean
  error: string | null
  appInfo: AppInfo | null
  health: HealthCheck | null

  // Actions
  setCurrentConversation: (conversation: Conversation | null) => void
  setMessages: (messages: Message[]) => void
  addMessage: (message: Message) => void
  setConversations: (conversations: Conversation[]) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  setAppInfo: (info: AppInfo) => void
  setHealth: (health: HealthCheck) => void
}

export const useChatStore = create<ChatStore>((set) => ({
  currentConversation: null,
  messages: [],
  conversations: [],
  isLoading: false,
  error: null,
  appInfo: null,
  health: null,

  setCurrentConversation: (conversation: Conversation | null) => set({ currentConversation: conversation }),
  setMessages: (messages: Message[]) => set({ messages }),
  addMessage: (message: Message) => set((state: ChatStore) => ({ messages: [...state.messages, message] })),
  setConversations: (conversations: Conversation[]) => set({ conversations }),
  setLoading: (loading: boolean) => set({ isLoading: loading }),
  setError: (error: string | null) => set({ error }),
  setAppInfo: (info: AppInfo) => set({ appInfo: info }),
  setHealth: (health: HealthCheck) => set({ health }),
}))

interface NotesStore {
  notes: Note[]
  isLoading: boolean
  error: string | null

  setNotes: (notes: Note[]) => void
  addNote: (note: Note) => void
  removeNote: (id: string) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
}

export const useNotesStore = create<NotesStore>((set) => ({
  notes: [],
  isLoading: false,
  error: null,

  setNotes: (notes: Note[]) => set({ notes }),
  addNote: (note: Note) => set((state: NotesStore) => ({ notes: [...state.notes, note] })),
  removeNote: (id: string) => set((state: NotesStore) => ({ notes: state.notes.filter((n) => n.id !== id) })),
  setLoading: (loading: boolean) => set({ isLoading: loading }),
  setError: (error: string | null) => set({ error }),
}))
