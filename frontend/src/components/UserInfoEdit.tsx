import React, { useState } from 'react'
import { Modal, Form, Input, Upload, Avatar, message } from 'antd'
import { UserOutlined, UploadOutlined } from '@ant-design/icons'
import type { UploadProps } from 'antd'
import Button from './ui/Button'

interface UserInfoEditProps {
  visible: boolean
  onCancel: () => void
  onSave: (values: any) => void
  initialValues?: {
    username: string
    email: string
    avatar?: string
  }
}

const UserInfoEdit: React.FC<UserInfoEditProps> = ({
  visible,
  onCancel,
  onSave,
  initialValues
}) => {
  const [form] = Form.useForm()
  const [avatarUrl, setAvatarUrl] = useState<string>(initialValues?.avatar || '')
  const [uploading, setUploading] = useState(false)

  const handleAvatarUpload: UploadProps['customRequest'] = async (options) => {
    const { file, onSuccess, onError } = options
    setUploading(true)

    try {
      // 创建FormData对象
      const formData = new FormData()
      formData.append('file', file as File)

      // 上传到后端
      const response = await fetch('/api/upload/avatar', {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        const result = await response.json()
        setAvatarUrl(result.url)
        message.success('头像上传成功')
        onSuccess?.(result)
      } else {
        throw new Error('上传失败')
      }
    } catch (error) {
      message.error('头像上传失败')
      onError?.(error as Error)
    } finally {
      setUploading(false)
    }
  }

  const handleSave = async () => {
    try {
      const values = await form.validateFields()
      onSave({
        ...values,
        avatar: avatarUrl
      })
      message.success('用户信息更新成功')
    } catch (error) {
      console.error('表单验证失败:', error)
    }
  }

  const beforeUpload = (file: File) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
    if (!isJpgOrPng) {
      message.error('只能上传 JPG/PNG 格式的图片!')
      return false
    }
    const isLt2M = file.size / 1024 / 1024 < 2
    if (!isLt2M) {
      message.error('图片大小不能超过 2MB!')
      return false
    }
    return true
  }

  return (
    <Modal
      title="编辑个人信息"
      open={visible}
      onCancel={onCancel}
      onOk={handleSave}
      okText="保存"
      cancelText="取消"
      width={500}
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={initialValues}
      >
        <div className="text-center mb-6">
          <Avatar
            size={100}
            src={avatarUrl}
            icon={<UserOutlined />}
            className="mb-4"
          />
          <div>
            <Upload
              showUploadList={false}
              customRequest={handleAvatarUpload}
              beforeUpload={beforeUpload}
              accept="image/*"
            >
              <Button
                icon={<UploadOutlined />}
                loading={uploading}
                variant="outline"
                size="middle"
              >
                {uploading ? '上传中...' : '更换头像'}
              </Button>
            </Upload>
          </div>
        </div>

        <Form.Item
          label="用户名"
          name="username"
          rules={[
            { required: true, message: '请输入用户名' },
            { min: 2, max: 20, message: '用户名长度为2-20个字符' }
          ]}
        >
          <Input placeholder="请输入用户名" />
        </Form.Item>

        <Form.Item
          label="邮箱"
          name="email"
          rules={[
            { required: true, message: '请输入邮箱' },
            { type: 'email', message: '请输入有效的邮箱地址' }
          ]}
        >
          <Input placeholder="请输入邮箱" />
        </Form.Item>

        <Form.Item
          label="个人简介"
          name="bio"
        >
          <Input.TextArea
            placeholder="请输入个人简介"
            rows={3}
            maxLength={200}
            showCount
          />
        </Form.Item>
      </Form>
    </Modal>
  )
}

export default UserInfoEdit