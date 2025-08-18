import React from 'react'
import { Routes, Route } from 'react-router-dom'
import VideoMixer from './pages/VideoMixer'
import './App.css'
import './styles/global.css'

function App() {
  return (
    <Routes>
      <Route path="/" element={<VideoMixer />} />
    </Routes>
  )
}

export default App 