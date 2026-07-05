import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Chat Page
 */
import { useState } from 'react';
import { motion } from 'framer-motion';
import { apiClient } from '@/services/api';
import { useChatStore } from '@/context/store';
import './Chat.css';
const ChatPage = () => {
    const [inputValue, setInputValue] = useState('');
    const { currentConversation, messages, addMessage, isLoading, setLoading } = useChatStore();
    const handleSendMessage = async () => {
        if (!inputValue.trim())
            return;
        const userMessage = {
            role: 'user',
            content: inputValue,
        };
        addMessage(userMessage);
        setInputValue('');
        setLoading(true);
        try {
            const response = await apiClient.chat([...messages, userMessage], currentConversation?.id);
            addMessage(response.message);
        }
        catch (error) {
            console.error('Failed to send message:', error);
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsx("div", { className: "chat-page", children: _jsxs("div", { className: "chat-container", children: [_jsxs("div", { className: "messages-section", children: [messages.map((msg, idx) => (_jsx(motion.div, { className: `message ${msg.role}`, initial: { opacity: 0, y: 10 }, animate: { opacity: 1, y: 0 }, transition: { duration: 0.3 }, children: _jsx("div", { className: "message-content", children: msg.content }) }, idx))), isLoading && (_jsx(motion.div, { className: "message assistant", initial: { opacity: 0 }, animate: { opacity: 1 }, children: _jsx("div", { className: "message-content", children: _jsxs("span", { className: "typing-indicator", children: [_jsx("span", {}), _jsx("span", {}), _jsx("span", {})] }) }) }))] }), _jsx("div", { className: "input-section", children: _jsxs("div", { className: "input-wrapper", children: [_jsx("input", { type: "text", value: inputValue, onChange: (e) => setInputValue(e.target.value), onKeyDown: (e) => e.key === 'Enter' && handleSendMessage(), placeholder: "Ask me anything...", disabled: isLoading, className: "message-input" }), _jsx("button", { onClick: handleSendMessage, disabled: isLoading, className: "send-button", children: isLoading ? '...' : '→' })] }) })] }) }));
};
export default ChatPage;
