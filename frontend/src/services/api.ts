import axios from 'axios'
import type { 
  VideoFile, 
  AudioFile, 
  Script, 
  ProjectConfig, 
  GenerationTask,
  ApiResponse,
  DurationOption,
  VoiceOption,
  StyleConfig 
} from '../types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',  // 使用相对路径，通过Vite代理
  timeout: 120000,
})

// 文件上传
export const uploadVideo = async (file: File): Promise<VideoFile> => {
  const formData = new FormData()
  formData.append('video', file)
  
  const response = await api.post<ApiResponse<VideoFile>>('/upload/video', formData)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '上传失败')
  }
  
  const video = response.data.data!
  // 修正 uploadedAt 字段类型
  return {
    ...video,
    uploadedAt: new Date(video.uploadedAt)
  };
}

// 获取上传进度
export const getUploadProgress = async (taskId: string) => {
  try {
    console.log('发送进度查询请求，URL:', `/upload/progress/${taskId}`)
    console.log('完整URL:', `${api.defaults.baseURL}/upload/progress/${taskId}`)
    const response = await api.get(`/upload/progress/${taskId}`)
    console.log('进度查询响应:', response.data)
    return response.data
  } catch (error) {
    console.error('getUploadProgress API调用失败:', error)
    console.error('请求配置:', error.config)
    console.error('响应状态:', error.response?.status)
    console.error('响应数据:', error.response?.data)
    throw error
  }
}

// 带真实进度监控的文件上传
export const uploadVideoWithProgress = async (
  file: File, 
  onProgress?: (progress: number, loaded: number, total: number, speed?: string) => void
): Promise<VideoFile> => {
  const formData = new FormData()
  formData.append('video', file)
  
  console.log('开始上传文件:', file.name)
  
  // 先启动上传请求
  const uploadPromise = api.post<ApiResponse<VideoFile>>('/upload/video', formData, {
    onUploadProgress: (progressEvent) => {
      // 这里只显示HTTP传输进度
      if (progressEvent.total && onProgress) {
        const httpProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(httpProgress * 0.1, progressEvent.loaded, progressEvent.total, "上传到服务器...")
      }
    }
  })
  
    // 获取上传结果，包含task_id
  const response = await uploadPromise

  console.log('上传响应:', response.data)

  if (!response.data.success) {
    throw new Error(response.data.error || '上传失败')
  }

  const video = response.data.data!
  const taskId = video.task_id

  console.log('获取到task_id:', taskId)
  console.log('video对象:', video)
  console.log('video.task_id:', video.task_id)
  
  // 显示开始OSS上传状态
  if (onProgress) {
    onProgress(10, 0, file.size, "开始上传到OSS...")
  }
  
  // 使用后端实时进度监控
  if (onProgress && taskId) {
    console.log('启动实时进度监控，taskId:', taskId)
    let progressCheckInterval: NodeJS.Timeout
    let lastProgress = 10
    
    const checkProgress = async () => {
      try {
        const progressData = await getUploadProgress(taskId)
        if (progressData.success) {
          const progress = progressData.data.progress || 0
          const speed = progressData.data.speed || "0 MB/s"
          
          // 避免进度倒退
          const currentProgress = Math.max(lastProgress, progress)
          lastProgress = currentProgress
          
          // 减少控制台日志输出，只在关键节点显示
          if (progress % 25 === 0 || progress >= 95) {
            console.log(`上传进度: ${currentProgress}%, 速度: ${speed}`)
          }
          
          onProgress(currentProgress, (currentProgress / 100) * fileSize, fileSize, speed)
          
          // 上传完成
          if (progress >= 100) {
            clearInterval(progressCheckInterval)
            onProgress(100, fileSize, fileSize, "上传完成")
            console.log('上传完成')
          }
        }
      } catch (error) {
        // 如果获取进度失败，使用估算进度
        console.warn('获取实时进度失败，使用估算进度')
        const elapsed = Date.now() - Date.now()
        const estimatedProgress = Math.min(95, lastProgress + 2)
        lastProgress = estimatedProgress
        onProgress(estimatedProgress, (estimatedProgress / 100) * fileSize, fileSize, "上传中...")
      }
    }
    
    // 开始监控，每2秒检查一次
    progressCheckInterval = setInterval(checkProgress, 2000)
    
    // 30秒后如果还没完成，自动结束监控
    setTimeout(() => {
      if (progressCheckInterval) {
        clearInterval(progressCheckInterval)
        onProgress(100, fileSize, fileSize, "上传完成")
      }
    }, 30000)
  }

  // 修正 uploadedAt 字段类型
  return {
    ...video,
    uploadedAt: new Date(video.uploadedAt)
  };
}

export const uploadAudio = async (file: File): Promise<AudioFile> => {
  const formData = new FormData()
  formData.append('audio', file)
  
  const response = await api.post<ApiResponse<AudioFile>>('/upload/audio', formData)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '上传失败')
  }
  
  return response.data.data!
}

// 带进度监控的音频上传
export const uploadAudioWithProgress = async (
  file: File, 
  onProgress?: (progress: number, loaded: number, total: number, speed?: string) => void
): Promise<AudioFile> => {
  const formData = new FormData()
  formData.append('audio', file)
  
  console.log('开始上传音频文件:', file.name)
  
  // 先启动上传请求
  const uploadPromise = api.post<ApiResponse<AudioFile>>('/upload/audio', formData, {
    onUploadProgress: (progressEvent) => {
      if (progressEvent.total && onProgress) {
        const httpProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(httpProgress * 0.1, progressEvent.loaded, progressEvent.total, "上传到服务器...")
      }
    }
  })
  
  const response = await uploadPromise

  if (!response.data.success) {
    throw new Error(response.data.error || '上传失败')
  }

  const audio = response.data.data!
  const taskId = audio.task_id

  console.log('获取到音频task_id:', taskId)
  
  // 显示开始OSS上传状态
  if (onProgress) {
    onProgress(10, 0, file.size, "开始上传到OSS...")
  }
  
  // 使用后端实时进度监控
  if (onProgress && taskId) {
    console.log('启动音频实时进度监控，taskId:', taskId)
    let progressCheckInterval: NodeJS.Timeout
    let lastProgress = 10
    
    const checkProgress = async () => {
      try {
        const progressData = await getUploadProgress(taskId)
        if (progressData.success) {
          const progress = progressData.data.progress || 0
          const speed = progressData.data.speed || "0 MB/s"
          
          const currentProgress = Math.max(lastProgress, progress)
          lastProgress = currentProgress
          
          if (progress % 25 === 0 || progress >= 95) {
            console.log(`音频进度: ${currentProgress}%, 速度: ${speed}`)
          }
          
          onProgress(currentProgress, (currentProgress / 100) * file.size, file.size, speed)
          
          if (progress >= 100) {
            clearInterval(progressCheckInterval)
            onProgress(100, file.size, file.size, "上传完成")
            console.log('音频上传完成')
          }
        }
      } catch (error) {
        console.warn('获取音频实时进度失败，使用估算进度')
        const estimatedProgress = Math.min(95, lastProgress + 5)
        lastProgress = estimatedProgress
        onProgress(estimatedProgress, (estimatedProgress / 100) * file.size, file.size, "上传中...")
      }
    }
    
    progressCheckInterval = setInterval(checkProgress, 2000)
    
    setTimeout(() => {
      if (progressCheckInterval) {
        clearInterval(progressCheckInterval)
        onProgress(100, file.size, file.size, "上传完成")
      }
    }, 20000)
  }

  return response.data.data!
}

// AI文案生成
export const generateScripts = async (
  base_script: string,
  video_duration: number,
  video_count: number
): Promise<Script[]> => {
  const response = await api.post<ApiResponse<Script[]>>('/ai/generate-scripts', {
    base_script,
    video_duration,
    video_count,
  })
  
  if (!response.data.success) {
    throw new Error(response.data.error || '生成失败')
  }
  
  return response.data.data!
}

// 项目配置
export const saveProject = async (config: Omit<ProjectConfig, 'id' | 'createdAt' | 'updatedAt'>): Promise<ProjectConfig> => {
  const response = await api.post<ApiResponse<ProjectConfig>>('/projects', config)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '保存失败')
  }
  
  return response.data.data!
}

export const getProject = async (id: string): Promise<ProjectConfig> => {
  const response = await api.get<ApiResponse<ProjectConfig>>(`/projects/${id}`)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '获取失败')
  }
  
  return response.data.data!
}

// 视频生成
export const startGeneration = async (projectId: string): Promise<GenerationTask> => {
  const response = await api.post<ApiResponse<GenerationTask>>('/generation/start', {
    projectId,
  })
  
  if (!response.data.success) {
    throw new Error(response.data.error || '启动失败')
  }
  
  return response.data.data!
}

export const getGenerationStatus = async (taskId: string): Promise<GenerationTask> => {
  const response = await api.get<ApiResponse<GenerationTask>>(`/generation/status/${taskId}`)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '获取状态失败')
  }
  
  return response.data.data!
}

// 文件删除
export const deleteVideo = async (id: string): Promise<void> => {
  const response = await api.delete<ApiResponse<void>>(`/videos/${id}`)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '删除失败')
  }
}

export const deleteAudio = async (id: string): Promise<void> => {
  const response = await api.delete<ApiResponse<void>>(`/audios/${id}`)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '删除失败')
  }
}

export default api