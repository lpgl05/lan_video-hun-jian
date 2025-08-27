// 视频文件信息
export interface VideoFile {
  id: string;
  name: string;
  url: string;
  size: number;
  duration: number;
  thumbnail?: string;
  uploadedAt: Date;
}

// 音频文件信息
export interface AudioFile {
  id: string;
  name: string;
  url: string;
  size: number;
  duration: number;
  uploadedAt: Date;
}

// 海报文件信息
export interface PosterFile {
  id: string;
  name: string;
  url: string;
  size: number;
  width?: number;
  height?: number;
  uploadedAt: Date;
}

// 文案信息
export interface Script {
  id: string;
  content: string;
  selected: boolean;
  generatedAt: Date;
}

// 时间设置选项
export type DurationOption = '15s' | '30s' | '30-60s';

// 语音朗读选项
export type VoiceOption = 'male' | 'female';

// 字体样式配置
export interface FontStyle {
  color: string;
  position: 'top' | 'center' | 'bottom' | 'template1';
  fontSize: number;
  fontFamily?: string;
  fontUrl?: string;
  bold?: boolean;
  italic?: boolean;
  shadow?: boolean;
  shadowColor?: string;
  strokeColor?: string;
  strokeWidth?: number;
}

// 主副标题配置（用于单个标题区域内的主副标题）
export interface TitleConfig {
  // 主标题
  mainTitle?: {
    text?: string;
    fontSize: number;
    color: string;
    fontFamily?: string;
    fontUrl?: string;
    bold?: boolean;
    italic?: boolean;
    shadow?: boolean;
    shadowColor?: string;
    strokeColor?: string;
    strokeWidth?: number;
  };
  // 副标题
  subTitle?: {
    text?: string;
    fontSize: number;
    color: string;
    fontFamily?: string;
    fontUrl?: string;
    bold?: boolean;
    italic?: boolean;
    shadow?: boolean;
    shadowColor?: string;
    strokeColor?: string;
    strokeWidth?: number;
  };
  // 整体配置
  position: 'top' | 'center' | 'bottom' | 'template1';
  spacing?: number; // 主副标题间距
  alignment?: 'left' | 'center' | 'right'; // 对齐方式
  background?: any; // 背景配置
  
  // 兼容旧版本的属性
  color?: string;
  fontSize?: number;
  fontFamily?: string;
  fontUrl?: string;
  bold?: boolean;
  italic?: boolean;
  shadow?: boolean;
  shadowColor?: string;
  strokeColor?: string;
  strokeWidth?: number;
}

// 样式配置
export interface StyleConfig {
  title: TitleConfig;
  subtitle: FontStyle;
}

// 项目配置
export interface ProjectConfig {
  id: string;
  name: string;
  videos: VideoFile[];
  audios: AudioFile[];
  posters: PosterFile[];
  scripts: Script[];
  duration: DurationOption;
  videoCount: number;
  voice: VoiceOption;
  style: StyleConfig;
  createdAt: Date;
  updatedAt: Date;
}

// 生成任务状态
export type TaskStatus = 'pending' | 'processing' | 'completed' | 'failed';

// 生成任务
export interface GenerationTask {
  id: string;
  projectId: string;
  status: TaskStatus;
  progress: number;
  result?: {
    videos: string[];
    previewUrl?: string;
  };
  error?: string;
  createdAt: string | Date; // 兼容后端返回的ISO字符串和前端Date对象
  updatedAt: string | Date; // 兼容后端返回的ISO字符串和前端Date对象
  generatedVideos?: VideoFile[]; // 添加详细视频信息
}

// API响应格式
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

// 上传进度
export interface UploadProgress {
  fileId: string;
  fileName: string;
  progress: number;
  status: 'uploading' | 'completed' | 'failed';
  error?: string;
}

// 项目历史记录
export interface ProjectHistory {
  id: string;
  name: string;
  status: TaskStatus;
  createdAt: string;
  completedAt?: string;
  videoCount: number;
  duration: DurationOption;
  videos?: VideoFile[];
  project: ProjectConfig; // 保存完整的项目配置
  task: GenerationTask; // 保存完整的任务信息
}