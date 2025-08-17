import React from 'react'
import { Button as AntButton, ButtonProps } from 'antd'
import { LoadingOutlined } from '@ant-design/icons'

interface BrixButtonProps extends Omit<ButtonProps, 'type' | 'variant'> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'small' | 'middle' | 'large'
  loading?: boolean
  fullWidth?: boolean
}

const Button: React.FC<BrixButtonProps> = ({
  variant = 'primary',
  size = 'middle',
  loading = false,
  fullWidth = false,
  children,
  style,
  ...props
}) => {
  const getVariantStyles = () => {
    const baseStyles = {
      borderRadius: '8px',
      fontWeight: '500',
      transition: 'all 0.2s ease',
      border: 'none',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '8px',
    }

    const sizeStyles = {
      small: {
        height: '32px',
        padding: '0 16px',
        fontSize: '14px',
      },
      middle: {
        height: '40px',
        padding: '0 20px',
        fontSize: '16px',
      },
      large: {
        height: '48px',
        padding: '0 24px',
        fontSize: '18px',
      },
    }

    const variantStyles = {
      primary: {
        background: 'linear-gradient(135deg, #4a3aff 0%, #6366f1 100%)',
        color: '#ffffff',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
      },
      secondary: {
        background: '#ffffff',
        color: '#111827',
        border: '1px solid #d1d5db',
        boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      },
      outline: {
        background: 'transparent',
        color: '#4a3aff',
        border: '1px solid #4a3aff',
      },
      ghost: {
        background: 'transparent',
        color: '#6b7280',
        border: 'none',
      },
      danger: {
        background: '#ef4444',
        color: '#ffffff',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
      },
    }

    return {
      ...baseStyles,
      ...sizeStyles[size],
      ...variantStyles[variant],
      ...(fullWidth && { width: '100%' }),
      ...(loading && { opacity: 0.7, cursor: 'not-allowed' }),
    }
  }

  const getAntdType = () => {
    switch (variant) {
      case 'primary':
        return 'primary'
      case 'danger':
        return 'primary'
      default:
        return 'default'
    }
  }

  return (
    <AntButton
      {...props}
      type={getAntdType()}
      loading={loading}
      style={{
        ...getVariantStyles(),
        ...style,
      }}
      icon={loading ? <LoadingOutlined /> : props.icon}
    >
      {children}
    </AntButton>
  )
}

export default Button
export type { BrixButtonProps }