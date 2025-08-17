import React, { useState, useEffect } from 'react'
import { Space, message } from 'antd'
import { ArrowLeftOutlined, ArrowRightOutlined } from '@ant-design/icons'
import { Button } from '../components/ui'
import StepWizard from '../components/StepWizard'
import BasicInfoStep from '../components/steps/BasicInfoStep'
import ContentUploadStep from '../components/steps/ContentUploadStep'
import ParameterConfigStep from '../components/steps/ParameterConfigStep'
import PreviewStep from '../components/steps/PreviewStep'
import type { 
  VideoFile, 
  AudioFile, 
  PosterFile,
  Script, 
  ProjectConfig, 
  GenerationTask,
  DurationOption,
  VoiceOption,
  StyleConfig 
} from '../types'
import { saveProject, startGeneration, getGenerationStatus } from '../services/api'

const VideoMixer: React.FC = () => {
  // 步骤状态
  const [currentStep, setCurrentStep] = useState(0)
  
  // 状态管理
  const [projectName, setProjectName] = useState('')
  const [videos, setVideos] = useState<VideoFile[]>([])
  const [audios, setAudios] = useState<AudioFile[]>([])
  const [posters, setPosters] = useState<PosterFile[]>([])
  const [usePoster, setUsePoster] = useState(false)
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
  
  // 步骤配置
  const steps = [
    { title: '基础信息', description: '项目名称配置' },
    { title: '内容上传', description: '视频、音频、海报素材' },
    { title: '参数配置', description: 'AI文案和生成设置' },
    { title: '预览确认', description: '确认配置并生成' }
  ]

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
        posters,
        usePoster,
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

  const canGenerate = videos.length > 0 && 
    scripts.filter(s => s.selected).length > 0 && 
    !generating

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

  // 步骤验证
  const validateStep = (step: number): boolean => {
    switch (step) {
      case 0: // 基础信息
        return projectName.trim().length > 0
      case 1: // 内容上传
        return videos.length > 0
      case 2: // 参数配置
        return scripts.filter(s => s.selected).length > 0
      case 3: // 预览确认
        return canGenerate
      default:
        return true
    }
  }

  // 步骤切换
  const handleStepChange = (step: number) => {
    if (step < currentStep || validateStep(currentStep)) {
      setCurrentStep(step)
    } else {
      message.warning('请完成当前步骤的必填项')
    }
  }

  // 下一步
  const handleNext = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, steps.length - 1))
    } else {
      message.warning('请完成当前步骤的必填项')
    }
  }

  // 上一步
  const handlePrev = () => {
    setCurrentStep(prev => Math.max(prev - 1, 0))
  }

  // 渲染当前步骤内容
  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        return (
          <BasicInfoStep
            projectName={projectName}
            onProjectNameChange={setProjectName}
          />
        )
      case 1:
        return (
          <ContentUploadStep
            videos={videos}
            onVideosChange={setVideos}
            audios={audios}
            onAudiosChange={setAudios}
            posters={posters}
            onPostersChange={setPosters}
            usePoster={usePoster}
            onUsePosterChange={setUsePoster}
          />
        )
      case 2:
        return (
          <ParameterConfigStep
            scripts={scripts}
            selectedScripts={scripts.filter(s => s.selected).map(s => s.id)}
            onScriptsChange={setScripts}
            duration={duration}
            onDurationChange={setDuration}
            quantity={videoCount}
            onQuantityChange={setVideoCount}
            voice={voice}
            onVoiceChange={setVoice}
            style={style}
            onStyleChange={setStyle}
          />
        )
      case 3:
        return (
          <PreviewStep
            projectName={projectName}
            videos={videos}
            audios={audios}
            posters={posters}
            usePoster={usePoster}
            scripts={scripts}
            selectedScripts={scripts.filter(s => s.selected).map(s => s.id)}
            duration={duration}
            videoCount={videoCount}
            voice={voice}
            style={style}
            onGenerate={handleStartGeneration}
            generating={generating}
            currentTask={currentTask || undefined}
            getProgressText={getProgressText}
          />
        )
      default:
        return null
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
        {/* 步骤导航 */}
        <StepWizard
          currentStep={currentStep}
          onStepChange={handleStepChange}
          steps={steps}
          className="mb-6"
        />

        {/* 步骤内容 */}
        <div className="step-container">
          {renderStepContent()}
        </div>

        {/* 步骤操作按钮 */}
        {currentStep < 3 && (
          <div className="step-actions mt-8 text-center">
            <Space size="large">
              {currentStep > 0 && (
                <Button
                  size="large"
                  variant="outline"
                  icon={<ArrowLeftOutlined />}
                  onClick={handlePrev}
                >
                  上一步
                </Button>
              )}
              <Button
                variant="primary"
                size="large"
                icon={<ArrowRightOutlined />}
                onClick={handleNext}
                disabled={!validateStep(currentStep)}
              >
                下一步
              </Button>
            </Space>
          </div>
        )}
      </div>
    </div>
  )
}

export default VideoMixer