/// <reference types="vite/client" />
/**
 * API client for SHAR-X AI backend
 */
import axios from 'axios';
class APIClient {
    constructor(baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000') {
        Object.defineProperty(this, "client", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: void 0
        });
        this.client = axios.create({
            baseURL,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }
    // Chat endpoints
    async chat(messages, conversationId) {
        const response = await this.client.post('/api/chat/', {
            messages,
            conversation_id: conversationId,
        });
        return response.data;
    }
    async getConversations() {
        const response = await this.client.get('/api/chat/conversations');
        return response.data;
    }
    async getConversation(id) {
        const response = await this.client.get(`/api/chat/conversations/${id}`);
        return response.data;
    }
    // System endpoints
    async getHealth() {
        const response = await this.client.get('/api/system/health');
        return response.data;
    }
    async getSystemStats() {
        const response = await this.client.get('/api/system/stats');
        return response.data;
    }
    async getAppInfo() {
        const response = await this.client.get('/api/system/info');
        return response.data;
    }
    // Notes endpoints
    async createNote(title, content, tags = []) {
        const response = await this.client.post('/api/notes/', {
            title,
            content,
            tags,
        });
        return response.data;
    }
    async getNotes() {
        const response = await this.client.get('/api/notes/');
        return response.data;
    }
    async getNote(id) {
        const response = await this.client.get(`/api/notes/${id}`);
        return response.data;
    }
    async updateNote(id, title, content, tags) {
        const response = await this.client.put(`/api/notes/${id}`, {
            title,
            content,
            tags,
        });
        return response.data;
    }
    async deleteNote(id) {
        await this.client.delete(`/api/notes/${id}`);
    }
    // Memory endpoints
    async addMemory(content, category = 'general') {
        const response = await this.client.post('/api/memory/add', {
            content,
            category,
        });
        return response.data;
    }
    async queryMemory(query, nResults = 5) {
        const response = await this.client.post('/api/memory/query', {
            query,
            n_results: nResults,
        });
        return response.data;
    }
    async getAllMemory() {
        const response = await this.client.get('/api/memory/all');
        return response.data;
    }
}
export const apiClient = new APIClient();
