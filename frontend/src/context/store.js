/**
 * Global state management with Zustand
 */
import { create } from 'zustand';
export const useChatStore = create((set) => ({
    currentConversation: null,
    messages: [],
    conversations: [],
    isLoading: false,
    error: null,
    appInfo: null,
    health: null,
    setCurrentConversation: (conversation) => set({ currentConversation: conversation }),
    setMessages: (messages) => set({ messages }),
    addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
    setConversations: (conversations) => set({ conversations }),
    setLoading: (loading) => set({ isLoading: loading }),
    setError: (error) => set({ error }),
    setAppInfo: (info) => set({ appInfo: info }),
    setHealth: (health) => set({ health }),
}));
export const useNotesStore = create((set) => ({
    notes: [],
    isLoading: false,
    error: null,
    setNotes: (notes) => set({ notes }),
    addNote: (note) => set((state) => ({ notes: [...state.notes, note] })),
    removeNote: (id) => set((state) => ({ notes: state.notes.filter((n) => n.id !== id) })),
    setLoading: (loading) => set({ isLoading: loading }),
    setError: (error) => set({ error }),
}));
