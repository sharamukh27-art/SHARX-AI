import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Settings Page
 */
import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { apiClient } from '@/services/api';
import { useChatStore } from '@/context/store';
import './Settings.css';
const SettingsPage = () => {
    const { appInfo, health } = useChatStore();
    const [stats, setStats] = React.useState(null);
    useEffect(() => {
        const fetchStats = async () => {
            try {
                const data = await apiClient.getSystemStats();
                setStats(data);
            }
            catch (error) {
                console.error('Failed to fetch system stats:', error);
            }
        };
        fetchStats();
        const interval = setInterval(fetchStats, 5000);
        return () => clearInterval(interval);
    }, []);
    return (_jsx("div", { className: "settings-page", children: _jsxs("div", { className: "settings-container", children: [_jsx("div", { className: "settings-header", children: _jsx("h1", { children: "Settings & System Info" }) }), _jsxs("div", { className: "settings-grid", children: [appInfo && (_jsxs(motion.div, { className: "settings-card", initial: { opacity: 0 }, animate: { opacity: 1 }, children: [_jsx("h2", { children: "Application" }), _jsxs("div", { className: "info-item", children: [_jsx("span", { className: "label", children: "Name:" }), _jsx("span", { className: "value", children: appInfo.app_name })] }), _jsxs("div", { className: "info-item", children: [_jsx("span", { className: "label", children: "Version:" }), _jsx("span", { className: "value", children: appInfo.version })] }), _jsxs("div", { className: "info-item", children: [_jsx("span", { className: "label", children: "Provider:" }), _jsx("span", { className: "value", children: appInfo.ai_provider })] })] })), health && (_jsxs(motion.div, { className: "settings-card", initial: { opacity: 0 }, animate: { opacity: 1 }, children: [_jsx("h2", { children: "System Health" }), _jsxs("div", { className: "info-item", children: [_jsx("span", { className: "label", children: "Status:" }), _jsx("span", { className: `value status-${health.status}`, children: health.status })] }), _jsxs("div", { className: "info-item", children: [_jsx("span", { className: "label", children: "AI Provider Available:" }), _jsx("span", { className: `value ${health.provider_available ? 'success' : 'error'}`, children: health.provider_available ? '✓ Yes' : '✗ No' })] })] })), stats && (_jsxs(motion.div, { className: "settings-card", initial: { opacity: 0 }, animate: { opacity: 1 }, children: [_jsx("h2", { children: "System Resources" }), _jsxs("div", { className: "info-item", children: [_jsx("span", { className: "label", children: "CPU Usage:" }), _jsxs("span", { className: "value", children: [stats.cpu_percent.toFixed(1), "%"] })] }), _jsxs("div", { className: "info-item", children: [_jsx("span", { className: "label", children: "Memory Usage:" }), _jsxs("span", { className: "value", children: [stats.memory.percent.toFixed(1), "%"] })] }), _jsxs("div", { className: "info-item", children: [_jsx("span", { className: "label", children: "Disk Usage:" }), _jsxs("span", { className: "value", children: [stats.disk.percent.toFixed(1), "%"] })] })] }))] })] }) }));
};
export default SettingsPage;
