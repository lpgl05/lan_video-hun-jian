import React, { useState, useEffect } from 'react'
import { message } from 'antd'
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
import MainLayout from '../components/MainLayout'
import LoginPage from '../components/LoginPage'
import StepWizard from '../components/StepWizard'
import UserCenter from '../components/UserCenter'
import GenerationResult from '../components/GenerationResult'
import GenerationModal from '../components/GenerationModal'
import { saveProject, startGeneration, getGenerationStatus } from '../services/api'

const VideoMixer: React.FC = () => {
  // 登录状态
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [userInfo, setUserInfo] = useState<{ phone: string; username: string } | null>(null)
  
  // 页面状态
  const [currentPage, setCurrentPage] = useState<'home' | 'user-center'>('home')
  
  // 弹窗状态
  const [showGenerationModal, setShowGenerationModal] = useState(false)
  
  // 数据状态管理
  const [projectName, setProjectName] = useState(() => {
    const now = new Date()
    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, '0')
    const day = String(now.getDate()).padStart(2, '0')
    return `${year}${month}${day}项目`
  })
  const [videos, setVideos] = useState<VideoFile[]>([])
  const [audios, setAudios] = useState<AudioFile[]>([])
  const [posters, setPosters] = useState<PosterFile[]>([])
  const [scripts, setScripts] = useState<Script[]>([])
  const [baseScript, setBaseScript] = useState('')
  const [duration, setDuration] = useState<DurationOption>('30s')
  const [videoCount, setVideoCount] = useState(3)
  const [voice, setVoice] = useState<VoiceOption>('female')
  const [style, setStyle] = useState<StyleConfig>({
    title: {
      color: '#1890ff',
      position: 'top',
      fontSize: 120,  // 默认120px
      fontFamily: 'Microsoft YaHei, sans-serif',
      strokeColor: '#000000',
      strokeWidth: 0,
      shadow: false,
      shadowColor: '#000000',
      bold: false,
      italic: false,
    },
    subtitle: {
      color: '#ffffff',
      position: 'bottom',
      fontSize: 60,  // 默认60px
      fontFamily: 'Microsoft YaHei, sans-serif',
      strokeColor: '#000000',
      strokeWidth: 1,
      shadow: true,
      shadowColor: '#000000',
      bold: false,
      italic: false,
    },
  })

  // 生成任务状态
  const [currentTask, setCurrentTask] = useState<GenerationTask | null>(null)
  const [generating, setGenerating] = useState(false)
  
  // 模拟未读通知数量
  const [unreadNotifications] = useState(2)

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
    setShowGenerationModal(true) // 显示生成弹窗

    try {
      // 1. 保存项目配置
      const project: Omit<ProjectConfig, 'id' | 'createdAt' | 'updatedAt'> = {
        name: projectName,
        videos,
        audios,
        posters,
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
      setShowGenerationModal(false) // 失败时关闭弹窗
    }
  }

  // 处理登录
  const handleLogin = (userInfo: { phone: string; username: string }) => {
    setIsLoggedIn(true)
    setUserInfo(userInfo)
  }

  // 处理退出登录
  const handleLogout = () => {
    setIsLoggedIn(false)
    setUserInfo(null)
    setCurrentPage('home')
    message.success('已退出登录')
  }

  // 处理生成完成
  const handleGenerationComplete = () => {
    setShowGenerationModal(false)
    setCurrentPage('home') // 返回主页面查看结果
  }

  // 处理重试生成
  const handleRetry = async () => {
    console.log('重新生成视频...')
    setShowGenerationModal(false) // 先关闭弹窗
    setCurrentTask(null) // 清空当前任务
    
    // 重新启动生成任务
    await handleStartGeneration()
  }

  // 新创作 - 清空所有数据
  const handleNewCreation = () => {
    setCurrentTask(null)
    const now = new Date()
    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, '0')
    const day = String(now.getDate()).padStart(2, '0')
    setProjectName(`${year}${month}${day}项目`)
    setVideos([])
    setAudios([])
    setPosters([])
    setScripts([])
    setBaseScript('')
    setDuration('30s')
    setVideoCount(3)
    setVoice('female')
    setStyle({
      title: {
        color: '#1890ff',
        position: 'top',
        fontSize: 120,  // 默认120px
        fontFamily: 'Microsoft YaHei, sans-serif',
        strokeColor: '#000000',
        strokeWidth: 0,
        shadow: false,
        shadowColor: '#000000',
        bold: false,
        italic: false,
      },
      subtitle: {
        color: '#ffffff',
        position: 'bottom',
        fontSize: 60,  // 默认60px
        fontFamily: 'Microsoft YaHei, sans-serif',
        strokeColor: '#000000',
        strokeWidth: 1,
        shadow: true,
        shadowColor: '#000000',
        bold: false,
        italic: false,
      },
    })
    message.success('已清空所有数据，可以开始新的创作！')
  }

  // 处理弹窗关闭
  const handleModalClose = () => {
    if (currentTask?.status === 'completed' || currentTask?.status === 'failed') {
      setShowGenerationModal(false)
    } else {
      // 如果任务还在进行中，允许后台运行
      setShowGenerationModal(false)
      message.info('任务将在后台继续运行')
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

  const renderPageContent = () => {
    if (currentPage === 'user-center') {
      return (
        <UserCenter 
          onBack={() => setCurrentPage('home')}
        />
      )
    }

    // 如果有正在进行的任务或已完成的任务，显示结果
    if (currentTask && (currentTask.status === 'processing' || currentTask.status === 'completed')) {
      return (
        <GenerationResult 
          task={currentTask}
          onReset={() => setCurrentTask(null)}
          onNewCreation={handleNewCreation}
        />
      )
    }

    // 默认显示分步向导
    return (
      <StepWizard
        projectName={projectName}
        setProjectName={setProjectName}
        videos={videos}
        setVideos={setVideos}
        audios={audios}
        setAudios={setAudios}
        posters={posters}
        setPosters={setPosters}
        scripts={scripts}
        setScripts={setScripts}
        baseScript={baseScript}
        setBaseScript={setBaseScript}
        duration={duration}
        setDuration={setDuration}
        videoCount={videoCount}
        setVideoCount={setVideoCount}
        voice={voice}
        setVoice={setVoice}
        style={style}
        setStyle={setStyle}
        onGenerate={handleStartGeneration}
        generating={generating}
      />
    )
  }

  // 如果未登录，显示登录页面
  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />
  }

  return (
    <>
      <MainLayout
        currentPage={currentPage}
        onPageChange={setCurrentPage}
        onLogout={handleLogout}
        unreadNotifications={unreadNotifications}
      >
        {renderPageContent()}
      </MainLayout>
      
      {/* 生成弹窗 */}
      <GenerationModal
        visible={showGenerationModal}
        task={currentTask}
        onClose={handleModalClose}
        onComplete={handleGenerationComplete}
        onRetry={handleRetry}
      />
    </>
  )
}

export default VideoMixer