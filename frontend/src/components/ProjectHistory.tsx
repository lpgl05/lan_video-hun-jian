import React, { useState, useEffect } from 'react'
import { Table, Tag, Space, Modal, Typography, Image, Tooltip } from 'antd'
import { EyeOutlined, DownloadOutlined, DeleteOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import Card from './ui/Card'
import Button from './ui/Button'

const { Text } = Typography

interface Project {
  id: string
  name: string
  description: string
  status: 'completed' | 'processing' | 'failed'
  createdAt: string
  updatedAt: string
  videoUrl?: string
  thumbnailUrl?: string
  duration?: number
  fileSize?: number
}

const ProjectHistory: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(false)
  const [previewVisible, setPreviewVisible] = useState(false)
  const [previewProject, setPreviewProject] = useState<Project | null>(null)

  // 模拟数据
  useEffect(() => {
    setLoading(true)
    // 模拟API调用
    setTimeout(() => {
      setProjects([
        {
          id: '1',
          name: '产品宣传视频',
          description: '公司新产品的宣传混剪视频',
          status: 'completed',
          createdAt: '2024-12-20 14:30:00',
          updatedAt: '2024-12-20 15:45:00',
          videoUrl: '/uploads/videos/product_promo.mp4',
          thumbnailUrl: '/uploads/thumbnails/product_promo.jpg',
          duration: 120,
          fileSize: 45.6
        },
        {
          id: '2',
          name: '教程混剪',
          description: '软件使用教程视频合集',
          status: 'completed',
          createdAt: '2024-12-19 10:15:00',
          updatedAt: '2024-12-19 11:20:00',
          videoUrl: '/uploads/videos/tutorial_mix.mp4',
          thumbnailUrl: '/uploads/thumbnails/tutorial_mix.jpg',
          duration: 300,
          fileSize: 89.2
        },
        {
          id: '3',
          name: '活动回顾',
          description: '年终活动精彩瞬间回顾',
          status: 'processing',
          createdAt: '2024-12-21 09:00:00',
          updatedAt: '2024-12-21 09:00:00'
        },
        {
          id: '4',
          name: '品牌故事',
          description: '企业品牌发展历程',
          status: 'failed',
          createdAt: '2024-12-18 16:20:00',
          updatedAt: '2024-12-18 16:25:00'
        }
      ])
      setLoading(false)
    }, 1000)
  }, [])

  const getStatusTag = (status: Project['status']) => {
    const statusConfig = {
      completed: { color: 'green', text: '已完成' },
      processing: { color: 'blue', text: '处理中' },
      failed: { color: 'red', text: '失败' }
    }
    const config = statusConfig[status]
    return <Tag color={config.color}>{config.text}</Tag>
  }

  const formatFileSize = (sizeInMB: number) => {
    if (sizeInMB < 1) {
      return `${(sizeInMB * 1024).toFixed(1)} KB`
    }
    return `${sizeInMB.toFixed(1)} MB`
  }

  const formatDuration = (seconds: number) => {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }

  const handlePreview = (project: Project) => {
    setPreviewProject(project)
    setPreviewVisible(true)
  }

  const handleDownload = (project: Project) => {
    if (project.videoUrl) {
      const link = document.createElement('a')
      link.href = project.videoUrl
      link.download = `${project.name}.mp4`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  const handleDelete = (projectId: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个项目吗？此操作不可恢复。',
      okText: '删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: () => {
        setProjects(prev => prev.filter(p => p.id !== projectId))
        // TODO: 调用删除API
      }
    })
  }

  const columns: ColumnsType<Project> = [
    {
      title: '项目名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <div className="flex items-center gap-4">
          {record.thumbnailUrl && (
            <Image
              width={60}
              height={40}
              src={record.thumbnailUrl}
              alt={record.name}
              className="rounded-lg object-cover border border-gray-200"
              fallback="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMIAAADDCAYAAADQvc6UAAABRWlDQ1BJQ0MgUHJvZmlsZQAAKJFjYGASSSwoyGFhYGDIzSspCnJ3UoiIjFJgf8LAwSDCIMogwMCcmFxc4BgQ4ANUwgCjUcG3awyMIPqyLsis7PPOq3QdDFcvjV3jOD1boQVTPQrgSkktTgbSf4A4LbmgqISBgTEFyFYuLykAsTuAbJEioKOA7DkgdjqEvQHEToKwj4DVhAQ5A9k3gGyB5IxEoBmML4BsnSQk8XQkNtReEOBxcfXxUQg1Mjc0dyHgXNJBSWpFCYh2zi+oLMpMzyhRcASGUqqCZ16yno6CkYGRAQMDKMwhqj/fAIcloxgHQqxAjIHBEugw5sUIsSQpBobtQPdLciLEVJYzMPBHMDBsayhILEqEO4DxG0txmrERhM29nYGBddr//5/DGRjYNRkY/l7////39v///y4Dmn+LgeHANwDrkl1AuO+pmgAAADhlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABAAAAwqADAAQAAAABAAAAwwAAAAD9b/HnAAAHlklEQVR4Ae3dP3Ik1RnG4W+FgYxN"
            />
          )}
          <div>
            <div className="font-semibold text-gray-900 text-base mb-1">
              {text}
            </div>
            <Text className="text-gray-600 text-sm">
              {record.description}
            </Text>
          </div>
        </div>
      )
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => getStatusTag(status)
    },
    {
      title: '时长',
      dataIndex: 'duration',
      key: 'duration',
      width: 80,
      render: (duration) => duration ? formatDuration(duration) : '-'
    },
    {
      title: '文件大小',
      dataIndex: 'fileSize',
      key: 'fileSize',
      width: 100,
      render: (size) => size ? formatFileSize(size) : '-'
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      key: 'createdAt',
      width: 150,
      render: (date) => new Date(date).toLocaleDateString('zh-CN')
    },
    {
      title: '操作',
      key: 'actions',
      width: 150,
      render: (_, record) => (
        <Space>
          {record.status === 'completed' && record.videoUrl && (
            <>
              <Tooltip title="预览">
                <Button
                  variant="ghost"
                  size="small"
                  icon={<EyeOutlined />}
                  onClick={() => handlePreview(record)}
                />
              </Tooltip>
              <Tooltip title="下载">
                <Button
                  variant="ghost"
                  size="small"
                  icon={<DownloadOutlined />}
                  onClick={() => handleDownload(record)}
                />
              </Tooltip>
            </>
          )}
          <Tooltip title="删除">
            <Button
              variant="ghost"
              size="small"
              icon={<DeleteOutlined />}
              onClick={() => handleDelete(record.id)}
            />
          </Tooltip>
        </Space>
      )
    }
  ]

  return (
    <div>
      <Card 
        title="项目历史" 
        variant="default"
        padding="large"
      >
        <Table
          columns={columns}
          dataSource={projects}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个项目`
          }}
          className="[&_.ant-table-thead>tr>th]:bg-gray-50 [&_.ant-table-thead>tr>th]:text-gray-900 [&_.ant-table-tbody>tr:hover>td]:bg-gray-50 [&_.ant-table]:border-gray-200"
        />
      </Card>

      <Modal
        title="视频预览"
        open={previewVisible}
        onCancel={() => setPreviewVisible(false)}
        footer={null}
        width={800}
        className="rounded-xl"
        styles={{
          header: {
            background: '#f8fafc',
            borderBottom: '1px solid #e2e8f0',
            borderRadius: '12px 12px 0 0',
            padding: '24px'
          },
          body: {
            background: '#f8fafc',
            padding: '24px'
          }
        }}
      >
        {previewProject && (
          <div className="text-center">
            <video
              controls
              width="100%"
              height="400"
              src={previewProject.videoUrl}
              className="rounded-lg border border-gray-200 bg-white"
            >
              您的浏览器不支持视频播放。
            </video>
            <div className="mt-6">
              <Typography.Title 
                level={4}
                className="text-gray-900 mb-4"
              >
                {previewProject.name}
              </Typography.Title>
              <Typography.Text className="text-gray-600 text-base">
                {previewProject.description}
              </Typography.Text>
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}

export default ProjectHistory