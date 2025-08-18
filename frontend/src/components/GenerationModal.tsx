import React, { useEffect, useState } from 'react'
import { Modal, Space, Button, Typography } from 'antd'
import { 
  VideoCameraOutlined, 
  CheckCircleOutlined, 
  ExclamationCircleOutlined,
  LoadingOutlined,
  CloseOutlined
} from '@ant-design/icons'
import type { GenerationTask } from '../types'
import '../styles/GenerationModal.css'

const { Title, Text } = Typography

interface GenerationModalProps {
  visible: boolean
  task: GenerationTask | null
  onClose: () => void
  onComplete: () => void
}

const GenerationModal: React.FC<GenerationModalProps> = ({
  visible,
  task,
  onClose,
  onComplete
}) => {
  const [elapsedTime, setElapsedTime] = useState(0)

  // 计算已用时间
  useEffect(() => {
    if (!task || task.status !== 'processing') {
      setElapsedTime(0)
      return
    }

    const timer = setInterval(() => {
      setElapsedTime(prev => prev + 1)
    }, 1000)

    return () => clearInterval(timer)
  }, [task?.status])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const getStatusInfo = () => {
    if (!task) return { title: '准备中...', description: '正在初始化任务' }

    switch (task.status) {
      case 'processing':
        return {
          title: 'AI正在合成中',
          description: '预计5分钟，请耐心等待...',
          icon: <LoadingOutlined spin style={{ color: '#1890ff' }} />
        }
      case 'completed':
        return {
          title: '生成完成！',
          description: '您的视频已成功生成，可以查看和下载了',
          icon: <CheckCircleOutlined style={{ color: '#52c41a' }} />
        }
      case 'failed':
        return {
          title: '生成失败',
          description: '视频生成过程中出现错误，请重试',
          icon: <ExclamationCircleOutlined style={{ color: '#ff4d4f' }} />
        }
      default:
        return {
          title: '准备中...',
          description: '正在初始化任务',
          icon: <LoadingOutlined spin style={{ color: '#1890ff' }} />
        }
    }
  }

  const statusInfo = getStatusInfo()

  return (
    <Modal
      open={visible}
      title={null}
      footer={null}
      onCancel={onClose}
      width={520}
      centered
      className="generation-modal"
      maskClosable={false}
      closeIcon={
        task?.status === 'completed' || task?.status === 'failed' ? (
          <CloseOutlined />
        ) : null
      }
    >
      <div className="modal-content">
        {/* 头部图标和标题 */}
        <div className="modal-header">
          <div className="header-icon">
            <VideoCameraOutlined />
          </div>
          <Title level={3} className="modal-title">
            AI视频生成
          </Title>
        </div>

        {/* 状态显示 */}
        <div className="status-section">
          <div className="status-icon">
            {statusInfo.icon}
          </div>
          <div className="status-info">
            <Title level={4} className="status-title">
              {statusInfo.title}
            </Title>
            <Text className="status-description">
              {statusInfo.description}
            </Text>
          </div>
        </div>

        {/* 已用时间显示 */}
        {task?.status === 'processing' && (
          <div className="time-section" style={{ 
            textAlign: 'center', 
            padding: '20px 0', 
            borderTop: '1px solid #f0f0f0',
            borderBottom: '1px solid #f0f0f0' 
          }}>
            <Text type="secondary" style={{ fontSize: '16px' }}>
              已用时: {formatTime(elapsedTime)}
            </Text>
          </div>
        )}



        {/* 底部按钮 */}
        <div className="modal-footer">
          {task?.status === 'processing' && (
            <div style={{ textAlign: 'center' }}>
              <Button onClick={onClose} type="primary">
                后台运行
              </Button>
            </div>
          )}
          
          {task?.status === 'completed' && (
            <Space>
              <Button onClick={onClose}>
                关闭
              </Button>
              <Button type="primary" onClick={onComplete}>
                查看结果
              </Button>
            </Space>
          )}
          
          {task?.status === 'failed' && (
            <Space>
              <Button onClick={onClose}>
                关闭
              </Button>
              <Button type="primary" danger>
                重新生成
              </Button>
            </Space>
          )}
        </div>
      </div>
    </Modal>
  )
}

export default GenerationModal
