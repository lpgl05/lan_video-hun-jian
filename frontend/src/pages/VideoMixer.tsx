import React, { useState, useEffect } from 'react'
import { Button, message, Input, Space, Progress } from 'antd'
import { PlayCircleOutlined, SaveOutlined } from '@ant-design/icons'
import type { 
  VideoFile, 
  AudioFile, 
  Script, 
  ProjectConfig, 
  GenerationTask,
  DurationOption,
  VoiceOption,
  StyleConfig 
} from '../types'
import VideoUpload from '../components/VideoUpload'
import AudioUpload from '../components/AudioUpload'
import ScriptConfig from '../components/ScriptConfig'
import ConfigSettings from '../components/ConfigSettings'
import GenerationResult from '../components/GenerationResult'
import { saveProject, startGeneration, getGenerationStatus } from '../services/api'

const VideoMixer: React.FC = () => {
  // 状态管理
  const [projectName, setProjectName] = useState('')
  const [videos, setVideos] = useState<VideoFile[]>([])
  const [audios, setAudios] = useState<AudioFile[]>([])
  const [scripts, setScripts] = useState<Script[]>([])
  const [duration, setDuration] = useState<DurationOption>('30s')
  const [videoCount, setVideoCount] = useState(3)
  const [voice, setVoice] = useState<VoiceOption>('female')
  const [style, setStyle] = useState<StyleConfig>({
    title: {
      color: '#ffffff',
      position: 'top',
      fontSize: 24,
    },
    subtitle: {
      color: '#ffffff',
      position: 'bottom',
      fontSize: 18,
    },
  })

  // 生成任务状态
  const [currentTask, setCurrentTask] = useState<GenerationTask | null>(null)
  const [generating, setGenerating] = useState(false)

  // 轮询任务状态
  useEffect(() => {
    if (!currentTask || currentTask.status === 'completed' || currentTask.status === 'failed') {
      return
    }

    const interval = setInterval(async () => {
      try {
        const updatedTask = await getGenerationStatus(currentTask.id)
        setCurrentTask(updatedTask)
        
        if (updatedTask.status === 'completed' || updatedTask.status === 'failed') {
          setGenerating(false)
        }
      } catch (error) {
        console.error('Failed to get task status:', error)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [currentTask])

  const handleStartGeneration = async () => {
    // 验证输入
    if (!projectName.trim()) {
      message.error('请输入项目名称')
      return
    }

    if (videos.length === 0) {
      message.error('请至少上传一个视频')
      return
    }

    if (scripts.filter(s => s.selected).length === 0) {
      message.error('请至少选择一个文案')
      return
    }

    setGenerating(true)

    try {
      // 1. 保存项目配置
      const project: Omit<ProjectConfig, 'id' | 'createdAt' | 'updatedAt'> = {
        name: projectName,
        videos,
        audios,
        scripts: scripts.filter(s => s.selected),
        duration,
        videoCount,
        voice,
        style,
      }

      const savedProject = await saveProject(project)

      // 2. 立即启动生成任务（不等待完成）
      const task = await startGeneration(savedProject.id)
      setCurrentTask(task)
      
      message.success('视频生成任务已启动，请稍候...')
      
      // 3. 开始轮询任务状态（前端会自动轮询）
      
    } catch (error) {
      message.error('启动生成失败')
      console.error('Generation error:', error)
      setGenerating(false)
    }
  }

  const handleReset = () => {
    setCurrentTask(null)
    setGenerating(false)
  }

  const canGenerate = videos.length > 0 && 
    scripts.filter(s => s.selected).length > 0 && 
    !generating

  const parseDuration = (duration: string) => {
    if (duration.endsWith('s')) {
      return parseInt(duration)
    }
    // 例如 '30-60s' 取最小值
    if (duration.includes('-')) {
      return parseInt(duration.split('-')[0])
    }
    return 30
  }

  const getProgressText = () => {
    if (!currentTask) return ''
    
    switch (currentTask.status) {
      case 'processing':
        if (currentTask.progress <= 10) return '正在下载素材...'
        if (currentTask.progress <= 30) return '正在剪辑视频...'
        if (currentTask.progress <= 50) return '正在生成字幕...'
        if (currentTask.progress <= 70) return '正在添加音频...'
        if (currentTask.progress <= 90) return '正在上传视频...'
        return '即将完成...'
      case 'completed':
        return '生成完成！'
      case 'failed':
        return '生成失败'
      default:
        return ''
    }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">AI视频混剪</h1>
        <p className="page-subtitle">
          上传视频素材，配置文案和样式，一键生成专业混剪视频
        </p>
      </div>

      <div className="page-content">
        {/* 项目名称 */}
        <div className="section">
          <div className="section-content">
            <div className="form-item">
              <label className="form-label">项目名称</label>
              <Input
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="请输入项目名称"
                maxLength={50}
              />
            </div>
          </div>
        </div>

        {/* 视频上传 */}
        <VideoUpload 
          videos={videos}
          onVideosChange={setVideos}
          maxCount={20}
        />

        {/* 音频上传 */}
        <AudioUpload 
          audios={audios}
          onAudiosChange={setAudios}
        />

        {/* 文案配置 */}
        <ScriptConfig 
          scripts={scripts}
          onScriptsChange={setScripts}
          videoDuration={parseDuration(duration)}
          videoCount={videoCount}
        />

        {/* 配置设置 */}
        <ConfigSettings
          duration={duration}
          onDurationChange={setDuration}
          videoCount={videoCount}
          onVideoCountChange={setVideoCount}
          voice={voice}
          onVoiceChange={setVoice}
          style={style}
          onStyleChange={setStyle}
        />

        {/* 生成按钮 */}
        <div className="action-buttons">
          <Space direction="vertical" style={{ width: '100%' }}>
            <Space>
              <Button
                type="primary"
                size="large"
                icon={<PlayCircleOutlined />}
                loading={generating}
                disabled={!canGenerate}
                onClick={handleStartGeneration}
              >
                {generating ? '生成中...' : '开始AI制作'}
              </Button>
              <Button
                size="large"
                icon={<SaveOutlined />}
                disabled={!canGenerate}
              >
                保存配置
              </Button>
            </Space>
            
            {/* 进度条显示 */}
            {currentTask && generating && (
              <div style={{ width: '100%', marginTop: '16px' }}>
                <Progress
                  percent={currentTask.progress || 0}
                  status={currentTask.status === 'failed' ? 'exception' : 'active'}
                  strokeColor={{
                    '0%': '#108ee9',
                    '100%': '#87d068',
                  }}
                />
                <div style={{ 
                  textAlign: 'center', 
                  marginTop: '8px', 
                  color: '#666',
                  fontSize: '14px'
                }}>
                  {getProgressText()}
                </div>
              </div>
            )}
          </Space>
        </div>

        {/* 生成结果 */}
        <GenerationResult 
          task={currentTask}
          onReset={handleReset}
        />
      </div>
    </div>
  )
}

export default VideoMixer