import React, { useState } from 'react'
import { Layout, Menu } from 'antd'
import { UserOutlined, SettingOutlined, LogoutOutlined, HomeOutlined, VideoCameraOutlined, HistoryOutlined, QuestionCircleOutlined, DownOutlined } from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'

const { Header } = Layout

const AppHeader: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const [userMenuVisible, setUserMenuVisible] = useState(false)

  const navigationItems = [
    {
      key: '/',
      icon: <VideoCameraOutlined />,
      label: '视频制作'
    },
    {
      key: '/profile',
      icon: <UserOutlined />,
      label: '个人中心'
    },
    {
      key: '/history',
      icon: <HistoryOutlined />,
      label: '历史记录'
    },
    {
      key: '/help',
      icon: <QuestionCircleOutlined />,
      label: '帮助中心'
    }
  ]

  const handleNavClick = (key: string) => {
    navigate(key)
  }

  return (
    <Header style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 1000,
      background: 'var(--bg-primary)',
      borderBottom: '1px solid var(--border-light)',
      boxShadow: 'var(--shadow-sm)',
      padding: '0 var(--spacing-lg)',
      height: '64px'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        height: '100%',
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        {/* 左侧品牌区域 */}
        <div 
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--spacing-sm)',
            cursor: 'pointer',
            transition: 'var(--transition-fast)',
            marginRight: 'var(--spacing-2xl)'
          }}
          onClick={() => navigate('/')}
          onMouseEnter={(e) => e.currentTarget.style.opacity = '0.8'}
          onMouseLeave={(e) => e.currentTarget.style.opacity = '1'}
        >
          <div style={{
            width: '32px',
            height: '32px',
            background: 'var(--primary-gradient)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--text-inverse)',
            fontWeight: 'var(--font-weight-bold)',
            fontSize: 'var(--font-size-base)'
          }}>
            V
          </div>
          <h1 style={{
            fontSize: 'var(--font-size-xl)',
            fontWeight: 'var(--font-weight-semibold)',
            color: 'var(--text-primary)',
            margin: 0
          }}>
            AI视频混剪平台
          </h1>
        </div>
        
        {/* 主导航菜单 */}
        <nav style={{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--spacing-lg)',
          flex: 1
        }}>
          {navigationItems.map(item => (
            <button
              key={item.key}
              onClick={() => handleNavClick(item.key)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--spacing-sm)',
                padding: 'var(--spacing-sm) var(--spacing-md)',
                borderRadius: 'var(--radius-md)',
                transition: 'var(--transition-fast)',
                border: 'none',
                cursor: 'pointer',
                background: location.pathname === item.key ? 'rgba(74, 58, 255, 0.1)' : 'transparent',
                color: location.pathname === item.key ? 'var(--primary-color)' : 'var(--text-secondary)',
                fontWeight: location.pathname === item.key ? 'var(--font-weight-medium)' : 'var(--font-weight-normal)'
              }}
              onMouseEnter={(e) => {
                if (location.pathname !== item.key) {
                  e.currentTarget.style.background = 'rgba(74, 58, 255, 0.05)'
                  e.currentTarget.style.color = 'var(--primary-color)'
                }
              }}
              onMouseLeave={(e) => {
                if (location.pathname !== item.key) {
                  e.currentTarget.style.background = 'transparent'
                  e.currentTarget.style.color = 'var(--text-secondary)'
                }
              }}
            >
              {item.icon}
              <span style={{ fontSize: 'var(--font-size-sm)' }}>{item.label}</span>
            </button>
          ))}
        </nav>
        
        {/* 右侧操作区域 */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--spacing-md)',
          marginLeft: 'var(--spacing-lg)'
        }}>
          <button
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 'var(--spacing-sm)',
              padding: 'var(--spacing-sm) var(--spacing-md)',
              borderRadius: 'var(--radius-md)',
              transition: 'var(--transition-fast)',
              border: 'none',
              cursor: 'pointer',
              background: 'transparent',
              color: 'var(--text-secondary)'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(74, 58, 255, 0.05)'
              e.currentTarget.style.color = 'var(--primary-color)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
              e.currentTarget.style.color = 'var(--text-secondary)'
            }}
          >
            <SettingOutlined />
            <span style={{ fontSize: 'var(--font-size-sm)' }}>设置</span>
          </button>
          
          <button
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 'var(--spacing-sm)',
              padding: 'var(--spacing-sm) var(--spacing-md)',
              borderRadius: 'var(--radius-md)',
              transition: 'var(--transition-fast)',
              border: 'none',
              cursor: 'pointer',
              background: 'transparent',
              color: 'var(--text-tertiary)'
            }}
            title="退出登录"
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(74, 58, 255, 0.05)'
              e.currentTarget.style.color = 'var(--primary-color)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
              e.currentTarget.style.color = 'var(--text-tertiary)'
            }}
          >
            <LogoutOutlined />
            <span style={{ fontSize: 'var(--font-size-sm)' }}>退出</span>
          </button>
        </div>
      </div>
    </Header>
  )
}

export default AppHeader