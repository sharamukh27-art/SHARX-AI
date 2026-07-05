/**
 * Notes Page
 */

import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { apiClient } from '@/services/api'
import { useNotesStore } from '@/context/store'
import './Notes.css'

const NotesPage: React.FC = () => {
  const { notes, setNotes, setLoading } = useNotesStore()
  const [title, setTitle] = React.useState('')
  const [content, setContent] = React.useState('')

  useEffect(() => {
    const fetchNotes = async () => {
      setLoading(true)
      try {
        const data = await apiClient.getNotes()
        setNotes(data)
      } catch (error) {
        console.error('Failed to fetch notes:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchNotes()
  }, [setNotes, setLoading])

  const handleAddNote = async () => {
    if (!title.trim() || !content.trim()) return

    try {
      const newNote = await apiClient.createNote(title, content)
      setNotes([...notes, newNote])
      setTitle('')
      setContent('')
    } catch (error) {
      console.error('Failed to create note:', error)
    }
  }

  return (
    <div className="notes-page">
      <div className="notes-container">
        <div className="notes-header">
          <h1>Notes</h1>
        </div>

        <div className="notes-input">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Note title..."
            className="note-title-input"
          />
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Note content..."
            className="note-content-input"
          />
          <button onClick={handleAddNote} className="add-note-btn">
            Add Note
          </button>
        </div>

        <div className="notes-list">
          {notes.map((note) => (
            <motion.div
              key={note.id}
              className="note-item"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
            >
              <h3>{note.title}</h3>
              <p>{note.content}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default NotesPage
