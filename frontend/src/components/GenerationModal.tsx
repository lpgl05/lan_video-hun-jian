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
  const [currentStage, setCurrentStage] = useState(0)
  const [estimatedTime, setEstimatedTime] = useState(300) // 5分钟
  const [elapsedTime, setElapsedTime] = useState(0)

  const stages = [
    { name: '准备素材', icon: '📁', description: '分析上传的视频和音频文件' },
    { name: '生成文案', icon: '✍️', description: 'AI智能生成视频文案内容' },
    { name: '视频剪辑', icon: '✂️', description: '根据文案智能剪辑视频片段' },
    { name: '添加特效', icon: '✨', description: '添加标题、字幕和转场效果' },
    { name: '合成输出', icon: '🎬', description: '最终合成并输出视频文件' }
  ]

  // 根据任务进度更新当前阶段
  useEffect(() => {
    if (!task) return

    const progress = task.progress || 0
    let stage = 0
    
    if (progress >= 80) stage = 4
    else if (progress >= 60) stage = 3
    else if (progress >= 40) stage = 2
    else if (progress >= 20) stage = 1
    else if (progress >= 10) stage = 0

    setCurrentStage(stage)
  }, [task?.progress])

  // 计算估算时间
  useEffect(() => {
    if (!task || task.status !== 'processing') return

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
        const stage = stages[currentStage]
        return {
          title: `${stage.name}中...`,
          description: stage.description,
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
  const progress = task?.progress || 0
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

        {/* 阶段指示器 */}
        {task?.status === 'processing' && (
          <div className="stages-section">
            <div className="stages-list">
              {stages.map((stage, index) => (
                <div
                  key={index}
                  className={`stage-item ${
                    index < currentStage ? 'completed' : 
                    index === currentStage ? 'active' : 'pending'
                  }`}
                >
                  <div className="stage-icon">{stage.icon}</div>
                  <div className="stage-name">{stage.name}</div>
                </div>
              ))}
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
