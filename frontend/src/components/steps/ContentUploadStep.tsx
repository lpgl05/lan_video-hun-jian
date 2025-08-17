import React from 'react'
import { Switch, Space, message } from 'antd'
import { Card } from '../ui'
import VideoUpload from '../VideoUpload'
import AudioUpload from '../AudioUpload'
import PosterUpload from '../PosterUpload'
import type { VideoFile, AudioFile, PosterFile } from '../../types'

interface ContentUploadStepProps {
  videos: VideoFile[]
  onVideosChange: (videos: VideoFile[]) => void
  audios: AudioFile[]
  onAudiosChange: (audios: AudioFile[]) => void
  posters: PosterFile[]
  onPostersChange: (posters: PosterFile[]) => void
  usePoster: boolean
  onUsePosterChange: (usePoster: boolean) => void
}

const ContentUploadStep: React.FC<ContentUploadStepProps> = ({
  videos,
  onVideosChange,
  audios,
  onAudiosChange,
  posters,
  onPostersChange,
  usePoster,
  onUsePosterChange
}) => {
  const handlePosterUploadSuccess = (poster: PosterFile) => {
    onPostersChange([...posters, poster])
    message.success('海报上传成功！')
  }

  const handlePosterDelete = (posterId: string) => {
    onPostersChange(posters.filter(p => p.id !== posterId))
  }

  return (
    <div className="step-content">
      <div className="flex flex-col gap-8">
        {/* 视频上传 */}
        <VideoUpload 
          videos={videos}
          onVideosChange={onVideosChange}
          maxCount={20}
        />

        {/* 音频上传 */}
        <AudioUpload 
          audios={audios}
          onAudiosChange={onAudiosChange}
        />

        {/* 海报上传 */}
        <Card 
          title="背景海报" 
          variant="default"
          padding="large"
          className="step-card"
        >
          <div className="mb-4">
            <Space align="center">
              <span className="text-sm text-gray-600 font-medium">启用海报背景</span>
              <Switch 
                checked={usePoster}
                onChange={onUsePosterChange}
                size="small"
                className={usePoster ? 'bg-purple-600' : 'bg-gray-300'}
              />
            </Space>
          </div>
          
          {usePoster && (
            <div>
              <Card 
                variant="default"
                padding="medium"
                className="upload-card"
              >
                <PosterUpload
                  onUploadSuccess={handlePosterUploadSuccess}
                  onDelete={handlePosterDelete}
                  maxCount={1}
                  disabled={false}
                />
              </Card>
              
              <div className="mt-2">
                <p className="text-xs text-gray-600 leading-normal m-0">
                  上传的海报将作为视频背景，建议使用高质量图片以获得最佳效果
                </p>
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}

export default ContentUploadStep