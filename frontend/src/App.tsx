import { Routes, Route } from 'react-router-dom'
import { Layout } from 'antd'
import AppHeader from './components/AppHeader'
import VideoMixer from './pages/VideoMixer'
import Profile from './pages/Profile'
import './App.css'

const { Content } = Layout

function App() {
  return (
    <Layout className="app-layout">
      <AppHeader />
      <Content className="app-content">
        <Routes>
          <Route path="/" element={<VideoMixer />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Content>
    </Layout>
  )
}

export default App