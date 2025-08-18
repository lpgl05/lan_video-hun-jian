import axios from 'axios'
import type {
  VideoFile,
  AudioFile,
  PosterFile,
  Script,
  ProjectConfig,
  GenerationTask,
  ApiResponse
} from '../types'

// 获取后端API地址
const getApiBaseUrl = () => {
  // 如果环境变量中设置了API地址，直接使用
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }
  
  // 自动检测当前访问方式
  const currentHost = window.location.hostname
  
  // 如果是通过IP访问的，使用相同的IP访问后端
  if (currentHost !== 'localhost' && currentHost !== '127.0.0.1') {
    return `http://${currentHost}:8000`
  }
  
  // 默认使用localhost
  return 'http://localhost:8000'
}

const api = axios.create({
  baseURL: getApiBaseUrl() + '/api',
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

export const uploadAudio = async (file: File): Promise<AudioFile> => {
  const formData = new FormData()
  formData.append('audio', file)
  
  const response = await api.post<ApiResponse<AudioFile>>('/upload/audio', formData)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '上传失败')
  }
  
  return response.data.data!
}

export const uploadPoster = async (file: File): Promise<PosterFile> => {
  const formData = new FormData()
  formData.append('poster', file)
  
  const response = await api.post<ApiResponse<PosterFile>>('/upload/poster', formData)
  
  if (!response.data.success) {
    throw new Error(response.data.error || '上传失败')
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