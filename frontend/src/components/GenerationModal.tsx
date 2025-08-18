import React, { useEffect, useState } from 'react'
import { Modal, Progress, Space, Button, Typography } from 'antd'
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
  const [estimatedTime] = useState(300) // 5分钟
  const [elapsedTime, setElapsedTime] = useState(0)
  const [simulatedProgress, setSimulatedProgress] = useState(0)



  // 计算估算时间
  useEffect(() => {
    if (!task || task.status !== 'processing') return

    const timer = setInterval(() => {
      setElapsedTime(prev => prev + 1)
    }, 1000)

    return () => clearInterval(timer)
  }, [task?.status])

  // 模拟进度条
  useEffect(() => {
    if (!task || task.status !== 'processing') {
      setSimulatedProgress(0)
      return
    }

    // 重置进度
    setSimulatedProgress(0)
    
    const progressInterval = setInterval(() => {
      setSimulatedProgress(prev => {
        if (prev >= 90) {
          return Math.min(prev + 0.3, 95) // 90%后缓慢增长，最大到95%
        }
        const increment = Math.random() * 2 + 0.5 // 0.5-2.5%的随机增长
        return Math.min(prev + increment, 90) // 确保线性增长到90%
      })
    }, 500)

    return () => clearInterval(progressInterval)
  }, [task?.status])

  // 任务完成时设置进度为100%
  useEffect(() => {
    if (task?.status === 'completed') {
      setSimulatedProgress(100)
    }
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
  const progress = task?.status === 'completed' ? 100 : simulatedProgress
  const remainingTime = Math.max(0, estimatedTime - elapsedTime)

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

        {/* 进度条 */}
        {task?.status === 'processing' && (
          <div className="progress-section">
            <Progress
              percent={progress}
              strokeColor={{
                '0%': '#1890ff',
                '50%': '#722ed1',
                '100%': '#52c41a'
              }}
              trailColor="#f0f0f0"
              size={8}
              className="custom-progress"
            />
            <div className="progress-info">
              <Text className="progress-text">
                {progress.toFixed(1)}% 完成
              </Text>
              <Text className="time-text">
                预计剩余时间: {formatTime(remainingTime)}
              </Text>
            </div>
          </div>
        )}



        {/* 底部按钮 */}
        <div className="modal-footer">
          {task?.status === 'processing' && (
            <Space>
              <Text type="secondary">
                已用时: {formatTime(elapsedTime)}
              </Text>
              <Button onClick={onClose} type="link">
                后台运行
              </Button>
            </Space>
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
