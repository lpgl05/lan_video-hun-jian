import React, { useState } from 'react';
import { Upload, Button, message, Image, Card, Progress, Space, Typography } from 'antd';
import { UploadOutlined, DeleteOutlined, EyeOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { uploadPoster } from '../services/api';
import type { PosterFile } from '../types';

const { Text } = Typography;

interface PosterUploadProps {
  onUploadSuccess?: (poster: PosterFile) => void;
  onDelete?: (posterId: string) => void;
  maxCount?: number;
  disabled?: boolean;
}

const PosterUpload: React.FC<PosterUploadProps> = ({
  onUploadSuccess,
  onDelete,
  maxCount = 1,
  disabled = false
}) => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [posters, setPosters] = useState<PosterFile[]>([]);
  const [previewVisible, setPreviewVisible] = useState(false);
  const [previewImage, setPreviewImage] = useState('');

  const handleUpload = async (file: File) => {
    // 文件类型验证
    const isImage = file.type.startsWith('image/');
    if (!isImage) {
      message.error('只能上传图片文件！');
      return false;
    }

    // 文件大小验证 (10MB)
    const isLt10M = file.size / 1024 / 1024 < 10;
    if (!isLt10M) {
      message.error('图片大小不能超过 10MB！');
      return false;
    }

    setUploading(true);
    setUploadProgress(0);

    try {
      // 模拟上传进度
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const posterFile = await uploadPoster(file);
      
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      // 添加到海报列表
      const newPoster = {
        ...posterFile,
        uploadedAt: new Date(posterFile.uploadedAt)
      };
      
      setPosters(prev => [...prev, newPoster]);
      onUploadSuccess?.(newPoster);
      
      message.success('海报上传成功！');
    } catch (error) {
      console.error('海报上传失败:', error);
      message.error(error instanceof Error ? error.message : '海报上传失败');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }

    return false; // 阻止默认上传行为
  };

  const handleDelete = (poster: PosterFile) => {
    setPosters(prev => prev.filter(p => p.id !== poster.id));
    onDelete?.(poster.id);
    message.success('海报删除成功');
  };

  const handlePreview = (poster: PosterFile) => {
    setPreviewImage(poster.url);
    setPreviewVisible(true);
  };

  const uploadProps: UploadProps = {
    beforeUpload: handleUpload,
    showUploadList: false,
    multiple: false,
    disabled: disabled || uploading || posters.length >= maxCount,
    accept: 'image/*'
  };

  return (
    <div className="poster-upload">
      <div className="mb-4">
        <Upload {...uploadProps}>
          <Button 
            icon={<UploadOutlined />} 
            loading={uploading}
            disabled={disabled || posters.length >= maxCount}
            size="large"
          >
            {uploading ? '上传中...' : '选择海报'}
          </Button>
        </Upload>
        
        {uploading && (
          <div className="mt-2">
            <Progress percent={uploadProgress} size="small" />
          </div>
        )}
        
        <div className="mt-2">
          <Text type="secondary" className="text-sm">
            支持 JPG、PNG、GIF 格式，文件大小不超过 10MB
          </Text>
        </div>
      </div>

      {/* 海报列表 */}
      {posters.length > 0 && (
        <div className="poster-list space-y-3">
          {posters.map((poster) => (
            <Card key={poster.id} size="small" className="poster-item">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="poster-thumbnail">
                    <Image
                      src={poster.url}
                      alt={poster.name}
                      width={60}
                      height={60}
                      className="object-cover rounded"
                      preview={false}
                    />
                  </div>
                  <div className="poster-info">
                    <div className="font-medium text-sm truncate max-w-[200px]">
                      {poster.name}
                    </div>
                    <div className="text-xs text-gray-500">
                      {poster.width} × {poster.height} • {(poster.size / 1024 / 1024).toFixed(2)} MB
                    </div>
                    <div className="text-xs text-gray-400">
                      {poster.uploadedAt.toLocaleString()}
                    </div>
                  </div>
                </div>
                
                <Space>
                  <Button
                    type="text"
                    icon={<EyeOutlined />}
                    size="small"
                    onClick={() => handlePreview(poster)}
                    title="预览"
                  />
                  <Button
                    type="text"
                    danger
                    icon={<DeleteOutlined />}
                    size="small"
                    onClick={() => handleDelete(poster)}
                    title="删除"
                  />
                </Space>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* 预览模态框 */}
      <Image
        style={{ display: 'none' }}
        src={previewImage}
        preview={{
          visible: previewVisible,
          onVisibleChange: setPreviewVisible,
        }}
      />
    </div>
  );
};

export default PosterUpload;