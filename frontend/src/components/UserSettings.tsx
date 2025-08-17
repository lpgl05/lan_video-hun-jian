import React, { useState } from 'react'
import { Form, Switch, Select, Radio, Slider, Divider, Space, message } from 'antd'
import { BellOutlined, EyeOutlined, GlobalOutlined, SaveOutlined } from '@ant-design/icons'
import Card from './ui/Card'
import Button from './ui/Button'

const { Option } = Select

interface UserSettingsData {
  theme: 'light' | 'dark' | 'auto'
  language: 'zh-CN' | 'en-US'
  notifications: {
    email: boolean
    push: boolean
    projectComplete: boolean
    systemUpdate: boolean
  }
  privacy: {
    profileVisible: boolean
    projectVisible: boolean
  }
  video: {
    defaultQuality: 'low' | 'medium' | 'high' | 'ultra'
    autoPlay: boolean
    volume: number
  }
  workspace: {
    autoSave: boolean
    saveInterval: number
    showTips: boolean
  }
}

const UserSettings: React.FC = () => {
  const [form] = Form.useForm()
  const [, setLoading] = useState(false)
  const [settings, setSettings] = useState<UserSettingsData>({
    theme: 'light',
    language: 'zh-CN',
    notifications: {
      email: true,
      push: true,
      projectComplete: true,
      systemUpdate: false
    },
    privacy: {
      profileVisible: true,
      projectVisible: false
    },
    video: {
      defaultQuality: 'high',
      autoPlay: false,
      volume: 80
    },
    workspace: {
      autoSave: true,
      saveInterval: 5,
      showTips: true
    }
  })

  const handleSave = async (values: any) => {
    setLoading(true)
    try {
      // 模拟保存设置
      await new Promise(resolve => setTimeout(resolve, 1000))
      setSettings(values)
      message.success('设置保存成功')
    } catch (error) {
      message.error('保存失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    form.resetFields()
    message.info('已重置为默认设置')
  }

  return (
    <div className="flex flex-col gap-8">
      <Form
        form={form}
        layout="vertical"
        initialValues={settings}
        onFinish={handleSave}
        style={{ maxWidth: '1024px' }}
      >
        {/* 外观设置 */}
        <Card 
          title={<><EyeOutlined className="mr-2 text-purple-600" />外观设置</>} 
          variant="default"
          padding="large"
        >
          <Form.Item label="主题模式" name="theme">
            <Radio.Group>
              <Radio value="light">浅色模式</Radio>
              <Radio value="dark">深色模式</Radio>
              <Radio value="auto">跟随系统</Radio>
            </Radio.Group>
          </Form.Item>

          <Form.Item label="语言设置" name="language">
            <Select className="w-48 rounded-lg border border-gray-200">
              <Option value="zh-CN">简体中文</Option>
              <Option value="en-US">English</Option>
            </Select>
          </Form.Item>
        </Card>

        {/* 通知设置 */}
        <Card 
          title={<><BellOutlined className="mr-2 text-purple-600" />通知设置</>} 
          variant="default"
          padding="large"
        >
          <Form.Item label="邮件通知" name={['notifications', 'email']} valuePropName="checked">
            <Switch />
          </Form.Item>

          <Form.Item label="推送通知" name={['notifications', 'push']} valuePropName="checked">
            <Switch />
          </Form.Item>

          <Form.Item label="项目完成通知" name={['notifications', 'projectComplete']} valuePropName="checked">
            <Switch />
          </Form.Item>

          <Form.Item label="系统更新通知" name={['notifications', 'systemUpdate']} valuePropName="checked">
            <Switch />
          </Form.Item>
        </Card>

        {/* 隐私设置 */}
        <Card 
          title={<><GlobalOutlined className="mr-2 text-purple-600" />隐私设置</>} 
          variant="default"
          padding="large"
        >
          <Form.Item 
            label="公开个人资料" 
            name={['privacy', 'profileVisible']} 
            valuePropName="checked"
            extra="允许其他用户查看您的基本信息"
          >
            <Switch />
          </Form.Item>

          <Form.Item 
            label="公开项目列表" 
            name={['privacy', 'projectVisible']} 
            valuePropName="checked"
            extra="允许其他用户查看您的项目列表"
          >
            <Switch />
          </Form.Item>
        </Card>

        {/* 视频设置 */}
        <Card 
          title="视频设置" 
          variant="default"
          padding="large"
        >
          <Form.Item label="默认视频质量" name={['video', 'defaultQuality']}>
            <Select className="w-48 rounded-lg border border-gray-200">
              <Option value="low">低质量 (480p)</Option>
              <Option value="medium">中等质量 (720p)</Option>
              <Option value="high">高质量 (1080p)</Option>
              <Option value="ultra">超高质量 (4K)</Option>
            </Select>
          </Form.Item>

          <Form.Item label="自动播放" name={['video', 'autoPlay']} valuePropName="checked">
            <Switch />
          </Form.Item>

          <Form.Item label="默认音量" name={['video', 'volume']}>
            <Slider
              min={0}
              max={100}
              marks={{
                0: '0%',
                50: '50%',
                100: '100%'
              }}
              className="w-72 mb-4"
              trackStyle={{ backgroundColor: '#4a3aff' }}
              handleStyle={{ borderColor: '#4a3aff' }}
            />
          </Form.Item>
        </Card>

        {/* 工作区设置 */}
        <Card 
          title="工作区设置" 
          variant="default"
          padding="large"
        >
          <Form.Item label="自动保存" name={['workspace', 'autoSave']} valuePropName="checked">
            <Switch />
          </Form.Item>

          <Form.Item label="保存间隔（分钟）" name={['workspace', 'saveInterval']}>
            <Select className="w-48 rounded-lg border border-gray-200">
              <Option value={1}>1分钟</Option>
              <Option value={3}>3分钟</Option>
              <Option value={5}>5分钟</Option>
              <Option value={10}>10分钟</Option>
              <Option value={15}>15分钟</Option>
            </Select>
          </Form.Item>

          <Form.Item label="显示操作提示" name={['workspace', 'showTips']} valuePropName="checked">
            <Switch />
          </Form.Item>
        </Card>

        <Divider />

        {/* 操作按钮 */}
        <div className="flex justify-end space-x-4 mb-8">
          <Button 
            icon={<SaveOutlined />} 
            variant="primary" 
            size="middle"
            onClick={handleSave}
          >
            保存设置
          </Button>
          <Button 
            variant="outline"
            size="middle"
            onClick={handleReset}
          >
            重置设置
          </Button>
        </div>
      </Form>

      {/* 危险操作区域 */}
      <Card 
        title="危险操作" 
        variant="outlined"
        padding="large"
        style={{
          borderColor: '#ff4d4f'
        }}
      >
        <Space direction="vertical" size="middle" className="w-full">
          <div>
            <h4 className="text-red-500 mb-2 text-base font-semibold">清除所有数据</h4>
            <p className="text-gray-600 mb-4 text-sm">这将删除您的所有项目和设置，此操作不可恢复。</p>
            <Button 
              variant="danger"
              size="middle"
            >
              清除数据
            </Button>
          </div>
          
          <Divider style={{ borderColor: '#ff4d4f', opacity: 0.3 }} />
          
          <div>
            <h4 className="text-red-500 mb-2 text-base font-semibold">停用账户</h4>
            <p className="text-gray-600 mb-4 text-sm">停用您的账户，您将无法再使用本服务。</p>
            <Button 
              variant="danger"
              size="middle"
            >
              停用账户
            </Button>
          </div>
        </Space>
      </Card>
    </div>
  )
}

export default UserSettings