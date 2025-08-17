import React, { useState, useEffect } from 'react'
import { Layout, Avatar, Typography, Row, Col, Statistic, Menu, List } from 'antd'
import { UserOutlined, ProjectOutlined, VideoCameraOutlined, SettingOutlined, HistoryOutlined, BarChartOutlined } from '@ant-design/icons'
import type { MenuProps } from 'antd'
import UserInfoEdit from '../components/UserInfoEdit'
import ProjectHistory from '../components/ProjectHistory'
import UsageStatistics from '../components/UsageStatistics'
import UserSettings from '../components/UserSettings'
import { Card, Button } from '../components/ui'

const { Content, Sider } = Layout
const { Title, Text } = Typography

type MenuItem = Required<MenuProps>['items'][number]

interface UserInfo {
  id: string
  username: string
  email: string
  avatar?: string
  createdAt: string
}

interface UserStats {
  totalProjects: number
  totalVideos: number
  totalDuration: number
}

const Profile: React.FC = () => {
  const [selectedKey, setSelectedKey] = useState('overview')
  const [editModalVisible, setEditModalVisible] = useState(false)
  const [userInfo, setUserInfo] = useState<UserInfo>({
    id: '1',
    username: '用户名',
    email: 'user@example.com',
    createdAt: '2024-01-01'
  })
  const [userStats] = useState<UserStats>({
    totalProjects: 0,
    totalVideos: 0,
    totalDuration: 0
  })

  const menuItems: MenuItem[] = [
    {
      key: 'overview',
      icon: <UserOutlined />,
      label: '概览'
    },
    {
      key: 'projects',
      icon: <ProjectOutlined />,
      label: '项目历史'
    },
    {
      key: 'statistics',
      icon: <BarChartOutlined />,
      label: '使用统计'
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '设置'
    }
  ]

  useEffect(() => {
    // TODO: 从API获取用户信息和统计数据
    // fetchUserInfo()
    // fetchUserStats()
  }, [])

  const handleEditUser = (values: any) => {
    setUserInfo(prev => ({
      ...prev,
      username: values.username,
      email: values.email,
      avatar: values.avatar
    }))
    setEditModalVisible(false)
    // TODO: 调用API更新用户信息
  }

  const renderOverview = () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
      <Card 
        variant="default"
        padding="large"
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-xl)' }}>
          <Avatar 
            size={100} 
            icon={<UserOutlined />} 
            src={userInfo.avatar}
            style={{
              background: 'var(--primary-gradient)',
              border: '4px solid var(--bg-primary)',
              boxShadow: 'var(--shadow-lg)'
            }}
          />
          <div style={{ flex: 1 }}>
            <Title 
              level={2} 
              style={{
                marginBottom: 'var(--spacing-sm)',
                color: 'var(--text-primary)',
                fontSize: 'var(--font-size-2xl)',
                fontWeight: 'var(--font-weight-bold)'
              }}
            >
              {userInfo.username}
            </Title>
            <Text 
              style={{
                color: 'var(--text-secondary)',
                fontSize: 'var(--font-size-base)',
                display: 'block',
                marginBottom: 'var(--spacing-xs)'
              }}
            >
              {userInfo.email}
            </Text>
            <Text 
              style={{
                color: 'var(--text-tertiary)',
                fontSize: 'var(--font-size-sm)'
              }}
            >
              注册时间: {userInfo.createdAt}
            </Text>
          </div>
          <div>
            <Button 
              variant="primary" 
              size="large"
              icon={<SettingOutlined />}
              onClick={() => setEditModalVisible(true)}
            >
              编辑资料
            </Button>
          </div>
        </div>
      </Card>

      <Row gutter={[24, 24]}>
        <Col xs={24} sm={8}>
          <Card
            variant="default"
            padding="medium"
          >
            <Statistic
              title="总项目数"
              value={userStats.totalProjects}
              prefix={<ProjectOutlined style={{ color: '#4a3aff', fontSize: '24px' }} />}
              valueStyle={{ 
                color: '#4a3aff',
                fontSize: '32px',
                fontWeight: '700'
              }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card
            variant="default"
            padding="medium"
          >
            <Statistic
              title="生成视频数"
              value={userStats.totalVideos}
              prefix={<VideoCameraOutlined style={{ color: '#10b981', fontSize: '24px' }} />}
              valueStyle={{ 
                color: '#10b981',
                fontSize: '32px',
                fontWeight: '700'
              }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card
            variant="default"
            padding="medium"
          >
            <Statistic
              title="总时长 (分钟)"
              value={userStats.totalDuration}
              prefix={<HistoryOutlined style={{ color: '#f59e0b', fontSize: '24px' }} />}
              valueStyle={{ 
                color: '#f59e0b',
                fontSize: '32px',
                fontWeight: '700'
              }}
            />
          </Card>
        </Col>
      </Row>

      <Card 
        variant="default"
        padding="large"
        title={
          <Title 
            level={4} 
            style={{
              margin: 0,
              color: '#111827',
              fontSize: '18px',
              fontWeight: '700'
            }}
          >
            最近活动
          </Title>
        }
      >
        <List
          dataSource={[
            { title: '创建了新项目 "产品宣传视频"', time: '2小时前', icon: <VideoCameraOutlined /> },
            { title: '完成视频生成 "教程混剪"', time: '1天前', icon: <ProjectOutlined /> },
          ]}
          renderItem={(item) => (
            <List.Item>
              <List.Item.Meta
                avatar={
                  <Avatar 
                    icon={item.icon}
                    style={{
                      background: '#ede9fe',
                      color: '#4a3aff',
                      border: '2px solid #ffffff'
                    }}
                  />
                }
                title={
                  <span style={{
                    color: '#111827',
                    fontSize: '16px',
                    fontWeight: '500'
                  }}>
                    {item.title}
                  </span>
                }
                description={
                  <span style={{
                    color: '#9ca3af',
                    fontSize: '14px'
                  }}>
                    {item.time}
                  </span>
                }
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  )

  const renderContent = () => {
    switch (selectedKey) {
      case 'overview':
        return renderOverview()
      case 'projects':
        return <ProjectHistory />
      case 'statistics':
        return <UsageStatistics />
      case 'settings':
        return <UserSettings />
      default:
        return renderOverview()
    }
  }

  return (
    <Layout style={{ minHeight: '100vh', background: '#f9fafb' }}>
      <Sider 
        width={280} 
        style={{
          background: '#ffffff',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
          borderRight: '1px solid #e5e7eb'
        }}
      >
        <div style={{
          padding: '24px',
          borderBottom: '1px solid #e5e7eb'
        }}>
          <Title 
            level={4} 
            style={{
              textAlign: 'center',
              marginBottom: '16px',
              color: '#111827',
              fontSize: '20px',
              fontWeight: '700'
            }}
          >
            个人中心
          </Title>
        </div>
        <Menu
          mode="inline"
          selectedKeys={[selectedKey]}
          items={menuItems}
          onClick={({ key }) => setSelectedKey(key)}
          style={{
            border: 'none',
            background: 'transparent',
            fontSize: '16px',
            fontWeight: '500'
          }}
          className="[&_.ant-menu-item-selected]:bg-purple-100 [&_.ant-menu-item]:text-gray-900 [&_.ant-menu-item-selected]:text-purple-600 [&_.ant-menu-item:hover]:bg-gray-50"
        />
      </Sider>
      <Layout>
        <Content style={{
          padding: '32px',
          background: '#f9fafb',
          minHeight: '100vh'
        }}>
          {renderContent()}
        </Content>
      </Layout>
      
      <UserInfoEdit
        visible={editModalVisible}
        onCancel={() => setEditModalVisible(false)}
        onSave={handleEditUser}
        initialValues={{
          username: userInfo.username,
          email: userInfo.email,
          avatar: userInfo.avatar
        }}
      />
    </Layout>
  )
}

export default Profile