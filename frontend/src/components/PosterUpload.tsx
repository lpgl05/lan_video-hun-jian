import React, { useState } from 'react'
import { Upload, Button, message, Modal, Progress, Switch, Card } from 'antd'
import { PictureOutlined, DeleteOutlined, EyeOutlined } from '@ant-design/icons'
import type { UploadProps } from 'antd/es/upload/interface'
import type { PosterFile } from '../types'
import { uploadPoster, uploadPosterWithProgress, deletePoster } from '../services/api'

interface PosterUploadProps {
  posters: PosterFile[]
  onPostersChange: (posters: PosterFile[]) => void
}

const PosterUpload: React.FC<PosterUploadProps> = ({ posters, onPostersChange }) => {
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadingFileName, setUploadingFileName] = useState('')
  const [uploadSpeed, setUploadSpeed] = useState('')
  const [previewVisible, setPreviewVisible] = useState(false)
  const [previewImage, setPreviewImage] = useState<string>('')
  const [enablePoster, setEnablePoster] = useState(false)

  const handleUpload = async (file: File) => {
    // 验证文件类型
    const isImage = file.type.startsWith('image/')
    if (!isImage) {
      message.error('只能上传图片文件！')
      return false
    }

    // 验证文件大小 (限制10MB)
    const isLt10M = file.size / 1024 / 1024 < 10
    if (!isLt10M) {
      message.error('图片大小不能超过10MB！')
      return false
    }

    setUploading(true)
    setUploadProgress(0)
    setUploadingFileName(file.name)
    setUploadSpeed('')

    try {
      const posterFile = await uploadPosterWithProgress(file, (progress, loaded, total, speed) => {
        setUploadProgress(progress)

        // 使用后端提供的速度信息，或者显示状态信息
        if (typeof speed === 'string') {
          setUploadSpeed(speed)
        } else if (speed) {
          setUploadSpeed(`${speed} MB/s`)
        }
      })

      onPostersChange([...posters, posterFile])
      message.success('海报上传成功')
    } catch (error) {
      message.error('海报上传失败')
      console.error('Upload error:', error)
    } finally {
      setUploading(false)
      setUploadProgress(0)
      setUploadingFileName('')
      setUploadSpeed('')
    }

    return false // 阻止默认上传行为
  }

  const handleDelete = async (posterId: string) => {
    try {
      await deletePoster(posterId)
      onPostersChange(posters.filter(poster => poster.id !== posterId))
      message.success('海报删除成功')
    } catch (error) {
      message.error('海报删除失败')
      console.error('Delete error:', error)
    }
  }

  const handlePreview = (posterUrl: string) => {
    setPreviewImage(posterUrl)
    setPreviewVisible(true)
  }

  const uploadProps: UploadProps = {
    accept: 'image/*',
    beforeUpload: handleUpload,
    disabled: uploading || !enablePoster,
    showUploadList: false,
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="section">
      <div className="section-title">
        <PictureOutlined />
        背景海报上传 ({posters.length})
      </div>

      <div className="section-content">
        <Card size="small" style={{ marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <Switch 
                checked={enablePoster}
                onChange={setEnablePoster}
                style={{ marginRight: '8px' }}
              />
              <span>启用背景海报 (选填)</span>
            </div>
            <span style={{ fontSize: '12px', color: '#666' }}>
              开启后可上传背景海报图片
            </span>
          </div>
        </Card>

        {enablePoster && (
          <>
            <Upload {...uploadProps}>
              <Button icon={<PictureOutlined />} loading={uploading} disabled={!enablePoster}>
                选择海报图片
              </Button>
            </Upload>

            {uploading && (
              <div style={{
                marginTop: '16px',
                padding: '12px',
                background: '#fafafa',
                borderRadius: '6px'
              }}>
                <div style={{ marginBottom: '8px', fontSize: '14px', color: '#666' }}>
                  正在上传: {uploadingFileName}
                </div>
                <Progress
                  percent={Math.round(uploadProgress * 10) / 10}
                  status="active"
                  format={(percent) => `${percent?.toFixed(1)}%`}
                />
                {uploadSpeed && (
                  <div style={{ marginTop: '4px', fontSize: '12px', color: '#999' }}>
                    {uploadSpeed}
                  </div>
                )}
              </div>
            )}

            <div className="upload-list">
              {posters.map((poster) => (
                <div key={poster.id} className="upload-item">
                  <div className="upload-item-content">
                    <div className="upload-item-preview">
                      <img 
                        src={poster.url}
                        alt={poster.name}
                        style={{ 
                          width: '60px',
                          height: '60px',
                          objectFit: 'cover',
                          borderRadius: '4px'
                        }}
                      />
                    </div>
                    <div className="upload-item-info">
                      <div className="upload-item-name">{poster.name}</div>
                      <div className="upload-item-meta">
                        <span>大小: {formatFileSize(poster.size)}</span>
                        {poster.width && poster.height && (
                          <span> • 尺寸: {poster.width}x{poster.height}</span>
                        )}
                        <span> • {new Date(poster.uploadedAt).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                  <div className="upload-item-actions">
                    <Button
                      type="text"
                      icon={<EyeOutlined />}
                      onClick={() => handlePreview(poster.url)}
                      title="预览"
                    />
                    <Button
                      type="text"
                      danger
                      icon={<DeleteOutlined />}
                      onClick={() => handleDelete(poster.id)}
                      title="删除"
                    />
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        <Modal
          open={previewVisible}
          title="海报预览"
          footer={null}
          onCancel={() => setPreviewVisible(false)}
          width="80%"
          style={{ top: 20 }}
        >
          <img
            alt="海报预览"
            style={{ width: '100%', maxHeight: '70vh', objectFit: 'contain' }}
            src={previewImage}
          />
        </Modal>
      </div>
    </div>
  )
}

export default PosterUpload
