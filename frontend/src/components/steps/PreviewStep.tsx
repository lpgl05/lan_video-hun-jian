import React from 'react'
import { Descriptions, Tag, Space, Progress } from 'antd'
import { PlayCircleOutlined, SaveOutlined } from '@ant-design/icons'
import GenerationResult from '../GenerationResult'
import { Script, GenerationTask } from '../../types'
import type { VideoFile, AudioFile, PosterFile, VoiceOption, StyleConfig, DurationOption } from '../../types'
import Card from '../ui/Card'
import Button from '../ui/Button'

interface PreviewStepProps {
  projectName: string
  videos: VideoFile[]
  audios: AudioFile[]
  posters: PosterFile[]
  usePoster: boolean
  scripts: Script[]
  selectedScripts: string[]
  duration: DurationOption
  videoCount: number
  voice: VoiceOption
  style: StyleConfig
  onGenerate: () => void
  generating: boolean
  currentTask?: GenerationTask
  getProgressText: () => string
}

const PreviewStep: React.FC<PreviewStepProps> = ({
  projectName,
  videos,
  audios,
  posters,
  usePoster,
  scripts,
  selectedScripts: selectedScriptIds,
  duration,
  videoCount,
  voice,
  style,
  onGenerate,
  generating,
  currentTask,
  getProgressText
}) => {
  const selectedScripts = scripts.filter(s => selectedScriptIds.includes(s.id))

  return (
    <div className="step-content">
      <div className="flex flex-col gap-8">
        {/* 配置预览 */}
        <Card 
          title="配置预览" 
          variant="default"
          padding="large"
        >
          <Descriptions 
            column={2} 
            bordered 
            size="small"
            className="bg-gray-50"
          >
            <Descriptions.Item label="项目名称" span={2}>
              <span className="text-gray-900 font-medium">
                {projectName || '未设置'}
              </span>
            </Descriptions.Item>
            <Descriptions.Item label="视频素材">
              <span className="text-gray-900">{videos.length} 个文件</span>
            </Descriptions.Item>
            <Descriptions.Item label="音频素材">
              <span className="text-gray-900">{audios.length} 个文件</span>
            </Descriptions.Item>
            <Descriptions.Item label="背景海报">
              <span className="text-gray-900">
                {usePoster ? `${posters.length} 个文件` : '未启用'}
              </span>
            </Descriptions.Item>
            <Descriptions.Item label="选中文案">
              <span className="text-gray-900">{selectedScripts.length} 条</span>
            </Descriptions.Item>
            <Descriptions.Item label="视频时长">
              <span className="text-gray-900">{duration}</span>
            </Descriptions.Item>
            <Descriptions.Item label="视频数量">
              <span className="text-gray-900">{videoCount} 个</span>
            </Descriptions.Item>
            <Descriptions.Item label="语音类型">
              <span className="text-gray-900">{voice}</span>
            </Descriptions.Item>
            <Descriptions.Item label="视频风格">
              <Tag 
                color="blue" 
                className="bg-purple-100 text-purple-600 border-purple-600 rounded"
              >
                {JSON.stringify(style)}
              </Tag>
            </Descriptions.Item>
          </Descriptions>
        </Card>

        {/* 选中的文案预览 */}
        {selectedScripts.length > 0 && (
          <Card 
            title="选中的文案" 
            variant="default"
            padding="large"
          >
            <div className="flex flex-col gap-2">
              {selectedScripts.map((script, index) => (
                <div 
                  key={script.id} 
                  className="p-4 bg-gray-50 rounded-lg border border-gray-200"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-900 mb-1">
                        文案 {index + 1}
                      </div>
                      <div className="text-sm text-gray-600 leading-normal">
                        {script.content}
                      </div>
                    </div>
                    <Tag 
                      color="green"
                      className="bg-green-100 text-green-600 border-green-600 rounded ml-2"
                    >
                      已选中
                    </Tag>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}

        {/* 生成按钮 */}
        <div className="action-buttons p-6 bg-gray-50 rounded-xl border border-gray-200 shadow-sm">
          <Space direction="vertical" className="w-full">
            <Space>
              <Button
                variant="primary"
                size="large"
                icon={<PlayCircleOutlined />}
                loading={generating}
                onClick={onGenerate}
              >
                {generating ? '生成中...' : '开始AI制作'}
              </Button>
              <Button
                variant="outline"
                size="large"
                icon={<SaveOutlined />}
                disabled={generating}
              >
                保存配置
              </Button>
            </Space>
            
            {/* 进度条显示 */}
            {currentTask && generating && (
              <div className="w-full mt-6">
                <Progress
                  percent={currentTask.progress || 0}
                  status={currentTask.status === 'failed' ? 'exception' : 'active'}
                  strokeColor={{
                    '0%': '#4a3aff',
                    '100%': '#10b981',
                  }}
                  trailColor="#f9fafb"
                  size="default"
                  className="bg-gray-50"
                />
                <div className="text-center mt-2 text-gray-600 text-sm font-medium">
                  {getProgressText()}
                </div>
              </div>
            )}
          </Space>
        </div>

        {/* 生成结果 */}
        <GenerationResult
            task={currentTask || null}
            onReset={() => {}}
          />
      </div>
    </div>
  )
}

export default PreviewStep