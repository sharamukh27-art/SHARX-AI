import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Notes Page
 */
import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { apiClient } from '@/services/api';
import { useNotesStore } from '@/context/store';
import './Notes.css';
const NotesPage = () => {
    const { notes, setNotes, setLoading } = useNotesStore();
    const [title, setTitle] = React.useState('');
    const [content, setContent] = React.useState('');
    useEffect(() => {
        const fetchNotes = async () => {
            setLoading(true);
            try {
                const data = await apiClient.getNotes();
                setNotes(data);
            }
            catch (error) {
                console.error('Failed to fetch notes:', error);
            }
            finally {
                setLoading(false);
            }
        };
        fetchNotes();
    }, [setNotes, setLoading]);
    const handleAddNote = async () => {
        if (!title.trim() || !content.trim())
            return;
        try {
            const newNote = await apiClient.createNote(title, content);
            setNotes([...notes, newNote]);
            setTitle('');
            setContent('');
        }
        catch (error) {
            console.error('Failed to create note:', error);
        }
    };
    return (_jsx("div", { className: "notes-page", children: _jsxs("div", { className: "notes-container", children: [_jsx("div", { className: "notes-header", children: _jsx("h1", { children: "Notes" }) }), _jsxs("div", { className: "notes-input", children: [_jsx("input", { type: "text", value: title, onChange: (e) => setTitle(e.target.value), placeholder: "Note title...", className: "note-title-input" }), _jsx("textarea", { value: content, onChange: (e) => setContent(e.target.value), placeholder: "Note content...", className: "note-content-input" }), _jsx("button", { onClick: handleAddNote, className: "add-note-btn", children: "Add Note" })] }), _jsx("div", { className: "notes-list", children: notes.map((note) => (_jsxs(motion.div, { className: "note-item", initial: { opacity: 0, scale: 0.95 }, animate: { opacity: 1, scale: 1 }, transition: { duration: 0.3 }, children: [_jsx("h3", { children: note.title }), _jsx("p", { children: note.content })] }, note.id))) })] }) }));
};
export default NotesPage;
