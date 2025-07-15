import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

// 組件
import Layout from './components/Layout'
import HomePage from './components/HomePage'
import LecturePage from './components/LecturePage'
import AdminPage from './components/AdminPage'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/lecture/:slug" element={<LecturePage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

