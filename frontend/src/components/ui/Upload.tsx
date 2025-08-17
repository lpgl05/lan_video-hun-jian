import React from 'react'
import { Upload as AntUpload, UploadProps, Button } from 'antd'
import { UploadOutlined, InboxOutlined, DeleteOutlined } from '@ant-design/icons'
import type { UploadFile } from 'antd/es/upload/interface'

interface BrixUploadProps extends UploadProps {
  variant?: 'button' | 'dragger' | 'card'
  uploadSize?: 'small' | 'medium' | 'large'
  error?: boolean
  helperText?: string
  showPreview?: boolean
}

const Upload: React.FC<BrixUploadProps> = ({
  variant = 'button',
  uploadSize = 'medium',
  error = false,
  helperText,
  showPreview = true,
  style,
  children,
  ...props
}) => {
  const getVariantStyles = () => {
    const baseStyles = {
      borderRadius: 'var(--radius-md)',
      transition: 'var(--transition-normal)',
      fontFamily: 'var(--font-family)',
    }

    const sizeStyles = {
      small: {
        minHeight: '80px',
        fontSize: 'var(--font-size-sm)',
      },
      medium: {
        minHeight: '120px',
        fontSize: 'var(--font-size-base)',
      },
      large: {
        minHeight: '160px',
        fontSize: 'var(--font-size-lg)',
      },
    }

    const variantStyles = {
      button: {
        ...baseStyles,
      },
      dragger: {
        ...baseStyles,
        ...sizeStyles[uploadSize],
        background: 'var(--bg-secondary)',
        border: `2px dashed ${error ? 'var(--error-color)' : 'var(--border-medium)'}`,
        padding: 'var(--spacing-lg)',
        textAlign: 'center' as const,
      },
      card: {
        ...baseStyles,
        ...sizeStyles[uploadSize],
        background: 'var(--bg-primary)',
        border: `1px solid ${error ? 'var(--error-color)' : 'var(--border-light)'}`,
        boxShadow: 'var(--shadow-sm)',
        padding: 'var(--spacing-md)',
      },
    }

    return variantStyles[variant]
  }

  const getButtonStyles = () => ({
    borderRadius: 'var(--radius-md)',
    background: 'var(--primary-gradient)',
    color: 'var(--text-inverse)',
    border: 'none',
    height: uploadSize === 'small' ? '32px' : uploadSize === 'large' ? '48px' : '40px',
    padding: `0 var(--spacing-${uploadSize === 'small' ? 'md' : uploadSize === 'large' ? 'xl' : 'lg'})`,
    fontWeight: 'var(--font-weight-medium)',
    boxShadow: 'var(--shadow-md)',
    transition: 'var(--transition-normal)',
  })

  const renderUploadContent = () => {
    if (variant === 'dragger') {
      return (
        <div style={{ color: 'var(--text-secondary)' }}>
          <div style={{ marginBottom: 'var(--spacing-md)' }}>
            <InboxOutlined style={{ fontSize: '48px', color: 'var(--primary-color)' }} />
          </div>
          <div style={{ fontSize: 'var(--font-size-lg)', marginBottom: 'var(--spacing-sm)' }}>
            点击或拖拽文件到此区域上传
          </div>
          <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-tertiary)' }}>
            支持单个或批量上传
          </div>
        </div>
      )
    }

    if (variant === 'card') {
      return (
        <div style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
          <UploadOutlined style={{ fontSize: '24px', color: 'var(--primary-color)', marginBottom: 'var(--spacing-sm)' }} />
          <div>选择文件上传</div>
        </div>
      )
    }

    return (
      <Button
        icon={<UploadOutlined />}
        style={getButtonStyles()}
      >
        {children || '上传文件'}
      </Button>
    )
  }

  const customItemRender = (originNode: React.ReactElement, file: UploadFile) => {
    if (!showPreview) return originNode

    return (
      <div
        style={{
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-light)',
          borderRadius: 'var(--radius-md)',
          padding: 'var(--spacing-md)',
          marginBottom: 'var(--spacing-sm)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <div style={{ flex: 1, color: 'var(--text-primary)' }}>
          {file.name}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
          {file.status === 'uploading' && (
            <div style={{ color: 'var(--primary-color)' }}>上传中...</div>
          )}
          {file.status === 'done' && (
            <div style={{ color: 'var(--success-color)' }}>✓</div>
          )}
          {file.status === 'error' && (
            <div style={{ color: 'var(--error-color)' }}>✗</div>
          )}
          <DeleteOutlined
            style={{ color: 'var(--text-tertiary)', cursor: 'pointer' }}
            onClick={() => {
              if (props.onRemove) {
                props.onRemove(file)
              }
            }}
          />
        </div>
      </div>
    )
  }

  if (variant === 'dragger') {
    return (
      <div style={{ width: '100%' }}>
        <AntUpload.Dragger
          {...props}
          style={{
            ...getVariantStyles(),
            ...style,
          }}
          itemRender={showPreview ? customItemRender : undefined}
        >
          {renderUploadContent()}
        </AntUpload.Dragger>
        {helperText && (
          <div
            style={{
              marginTop: 'var(--spacing-xs)',
              fontSize: 'var(--font-size-sm)',
              color: error ? 'var(--error-color)' : 'var(--text-tertiary)',
            }}
          >
            {helperText}
          </div>
        )}
      </div>
    )
  }

  return (
    <div style={{ width: '100%' }}>
      <AntUpload
        {...props}
        style={{
          ...getVariantStyles(),
          ...style,
        }}
        itemRender={showPreview ? customItemRender : undefined}
      >
        {renderUploadContent()}
      </AntUpload>
      {helperText && (
        <div
          style={{
            marginTop: 'var(--spacing-xs)',
            fontSize: 'var(--font-size-sm)',
            color: error ? 'var(--error-color)' : 'var(--text-tertiary)',
          }}
        >
          {helperText}
        </div>
      )}
    </div>
  )
}

export default Upload
export type { BrixUploadProps }