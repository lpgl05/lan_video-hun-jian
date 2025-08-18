import axios from 'axios'
import type { 
  VideoFile, 
  AudioFile, 
  PosterFile,
  Script, 
  ProjectConfig, 
  GenerationTask,
  ApiResponse,
  DurationOption,
  VoiceOption,
  StyleConfig 
} from '../types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',  // 使用空baseURL，让API路径包含完整路径
  timeout: 120000,
})

// 文件上传
export const uploadVideo = async (file: File): Promise<VideoFile> => {
  const formData = new FormData()
  formData.append('video', file)
  
  const response = await api.post<ApiResponse<VideoFile>>('/api/upload/video', formData)
  
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
    const response = await api.get(`/api/upload/progress/${taskId}`)
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

// 简化版本的文件上传 - 重写进度条逻辑
export const uploadVideoWithProgress = async (
  file: File, 
  onProgress?: (progress: number, loaded: number, total: number, speed?: string) => void
): Promise<VideoFile> => {
  const formData = new FormData()
  formData.append('video', file)
  
  console.log('开始上传文件:', file.name)
  
  if (onProgress) {
    onProgress(0, 0, file.size, "开始上传...")
  }

  try {
    // 使用模拟进度的方式，避免复杂的轮询逻辑
    let currentProgress = 0
    let progressInterval: NodeJS.Timeout | null = null
    let isUploadComplete = false
    
    // 启动模拟进度更新
    const startProgressSimulation = () => {
      if (progressInterval) return
      
      progressInterval = setInterval(() => {
        if (isUploadComplete || currentProgress >= 95) {
          return // 不超过95%，等待真实完成
        }
        
        // 根据文件大小调整进度速度
        const increment = file.size > 100 * 1024 * 1024 ? 2 : 5 // 大文件慢一点
        currentProgress = Math.min(95, currentProgress + increment)
        
        if (onProgress) {
          const speed = file.size > 50 * 1024 * 1024 ? "3.2 MB/s" : "1.8 MB/s"
          onProgress(currentProgress, (currentProgress / 100) * file.size, file.size, speed)
        }
      }, 800) // 每800ms更新一次
    }
    
    // 开始上传请求
    const uploadPromise = api.post<ApiResponse<VideoFile>>('/api/upload/video', formData, {
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const httpProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          
          if (httpProgress < 100) {
            // HTTP传输阶段：0-15%
            const displayProgress = Math.min(15, httpProgress * 0.15)
            onProgress(displayProgress, progressEvent.loaded, file.size, "传输到服务器...")
            currentProgress = displayProgress
          } else {
            // HTTP传输完成，开始模拟OSS上传进度
            if (currentProgress < 20) {
              currentProgress = 20
              if (onProgress) {
                onProgress(20, file.size * 0.2, file.size, "开始上传到云端...")
              }
            }
            // 启动模拟进度
            startProgressSimulation()
          }
        }
      }
    })

    // 等待上传完成
    const response = await uploadPromise
    
    // 清理进度模拟
    isUploadComplete = true
    if (progressInterval) {
      clearInterval(progressInterval)
      progressInterval = null
    }
    
    console.log('上传完成，响应:', response.data)

    if (!response.data.success) {
      throw new Error(response.data.error || '上传失败')
    }

    // 显示100%完成
    if (onProgress) {
      onProgress(100, file.size, file.size, "上传完成")
    }

    const video = response.data.data!
    return {
      ...video,
      uploadedAt: new Date(video.uploadedAt)
    }
    
  } catch (error) {
    console.error('上传失败:', error)
    throw error
  }
}

export const uploadAudio = async (file: File): Promise<AudioFile> => {
  const formData = new FormData()
  formData.append('audio', file)
  
  const response = await api.post<ApiResponse<AudioFile>>('/api/upload/audio', formData)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '上传失败')
  }
  
  return response.data.data!
}

// 简化版音频上传
export const uploadAudioWithProgress = async (
  file: File, 
  onProgress?: (progress: number, loaded: number, total: number, speed?: string) => void
): Promise<AudioFile> => {
  const formData = new FormData()
  formData.append('audio', file)
  
  console.log('开始上传音频文件:', file.name)
  
  if (onProgress) {
    onProgress(0, 0, file.size, "开始上传...")
  }

  try {
    // 简化的模拟进度逻辑
    let currentProgress = 0
    let progressInterval: NodeJS.Timeout | null = null
    let isUploadComplete = false
    
    const startProgressSimulation = () => {
      if (progressInterval) return
      
      progressInterval = setInterval(() => {
        if (isUploadComplete || currentProgress >= 95) {
          return
        }
        
        // 音频文件通常较小，进度更快一些
        const increment = file.size > 50 * 1024 * 1024 ? 3 : 8
        currentProgress = Math.min(95, currentProgress + increment)
        
        if (onProgress) {
          const speed = "2.1 MB/s"
          onProgress(currentProgress, (currentProgress / 100) * file.size, file.size, speed)
        }
      }, 600) // 音频上传稍快一些
    }
    
    // 启动上传请求
    const uploadPromise = api.post<ApiResponse<AudioFile>>('/api/upload/audio', formData, {
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const httpProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          
          if (httpProgress < 100) {
            // HTTP传输阶段：0-15%
            const displayProgress = Math.min(15, httpProgress * 0.15)
            onProgress(displayProgress, progressEvent.loaded, file.size, "传输到服务器...")
            currentProgress = displayProgress
          } else {
            // HTTP传输完成，开始模拟OSS上传进度
            if (currentProgress < 20) {
              currentProgress = 20
              if (onProgress) {
                onProgress(20, file.size * 0.2, file.size, "开始上传到云端...")
              }
            }
            startProgressSimulation()
          }
        }
      }
    })

    // 等待上传完成
    const response = await uploadPromise
    
    // 清理进度模拟
    isUploadComplete = true
    if (progressInterval) {
      clearInterval(progressInterval)
      progressInterval = null
    }
    
    console.log('音频上传完成，响应:', response.data)

    if (!response.data.success) {
      throw new Error(response.data.error || '音频上传失败')
    }

    // 显示100%完成
    if (onProgress) {
      onProgress(100, file.size, file.size, "上传完成")
    }

    const audio = response.data.data!
    return {
      ...audio,
      uploadedAt: new Date(audio.uploadedAt)
    }
    
  } catch (error) {
    console.error('音频上传失败:', error)
    throw error
  }
}

// 海报上传
export const uploadPoster = async (file: File): Promise<PosterFile> => {
  const formData = new FormData()
  formData.append('poster', file)

  const response = await api.post<ApiResponse<PosterFile>>('/api/upload/poster', formData)

  if (!response.data.success) {
    throw new Error(response.data.error || '上传失败')
  }

  return response.data.data!
}

// 带进度监控的海报上传
export const uploadPosterWithProgress = async (
  file: File,
  onProgress?: (progress: number, loaded: number, total: number, speed?: string) => void
): Promise<PosterFile> => {
  const formData = new FormData()
  formData.append('poster', file)

  console.log('开始上传海报文件:', file.name)

  const response = await api.post<ApiResponse<PosterFile>>('/api/upload/poster', formData, {
    onUploadProgress: (progressEvent) => {
      if (progressEvent.total && onProgress) {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(progress, progressEvent.loaded, progressEvent.total, "上传中...")
      }
    }
  })

  if (!response.data.success) {
    throw new Error(response.data.error || '上传失败')
  }

  console.log('海报上传完成')
  return response.data.data!
}

// 删除海报
export const deletePoster = async (posterId: string): Promise<void> => {
  const response = await api.delete<ApiResponse>(`/api/upload/poster/${posterId}`)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '删除失败')
  }
}

// AI文案生成
export const generateScripts = async (
  base_script: string,
  video_duration: number,
  video_count: number
): Promise<Script[]> => {
  const response = await api.post<ApiResponse<Script[]>>('/api/ai/generate-scripts', {
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
export const deleteVideo = async (id: string, url?: string): Promise<void> => {
  const params = url ? { file_url: url } : {}
  const response = await api.delete<ApiResponse<void>>(`/api/videos/${id}`, { params })
  
  if (!response.data.success) {
    throw new Error(response.data.error || '删除失败')
  }
}

export const deleteAudio = async (id: string, url?: string): Promise<void> => {
  const params = url ? { file_url: url } : {}
  const response = await api.delete<ApiResponse<void>>(`/api/audios/${id}`, { params })
  
  if (!response.data.success) {
    throw new Error(response.data.error || '删除失败')
  }
}

// 测试删除接口
export const testDelete = async (id: string): Promise<void> => {
  console.log('调用测试删除接口:', id)
  const response = await api.delete<ApiResponse<void>>(`/api/test/delete/${id}`)
  console.log('测试删除响应:', response.data)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '测试删除失败')
  }
}

export default api