import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Main App Component
 */
import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { apiClient } from '@/services/api';
import { useChatStore } from '@/context/store';
import ChatPage from '@/pages/Chat';
import SettingsPage from '@/pages/Settings';
import NotesPage from '@/pages/Notes';
import './App.css';
function App() {
    const { setAppInfo, setHealth } = useChatStore();
    useEffect(() => {
        const initializeApp = async () => {
            try {
                // Fetch app info
                const info = await apiClient.getAppInfo();
                setAppInfo(info);
                // Check health
                const health = await apiClient.getHealth();
                setHealth(health);
            }
            catch (error) {
                console.error('Failed to initialize app:', error);
            }
        };
        initializeApp();
    }, [setAppInfo, setHealth]);
    return (_jsx(Router, { children: _jsx("div", { className: "app-container", children: _jsxs(Routes, { children: [_jsx(Route, { path: "/", element: _jsx(ChatPage, {}) }), _jsx(Route, { path: "/notes", element: _jsx(NotesPage, {}) }), _jsx(Route, { path: "/settings", element: _jsx(SettingsPage, {}) })] }) }) }));
}
export default App;
