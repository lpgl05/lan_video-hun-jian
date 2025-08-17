import React from 'react'
import { Input as AntInput, InputProps } from 'antd'
import type { TextAreaProps } from 'antd/es/input'

interface BrixInputProps extends Omit<InputProps, 'variant'> {
  variant?: 'default' | 'filled' | 'outlined'
  inputSize?: 'small' | 'medium' | 'large'
  error?: boolean
  helperText?: string
}

interface BrixTextAreaProps extends Omit<TextAreaProps, 'variant'> {
  variant?: 'default' | 'filled' | 'outlined'
  error?: boolean
  helperText?: string
}

const Input: React.FC<BrixInputProps> = ({
  variant = 'default',
  inputSize = 'medium',
  error = false,
  helperText,
  style,
  ...props
}) => {
  const getVariantStyles = () => {
    const baseStyles = {
      borderRadius: '8px',
      transition: 'all 0.2s ease',
      fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
    }

    const sizeStyles = {
      small: {
        height: '32px',
        fontSize: '14px',
        padding: '0 12px',
      },
      medium: {
        height: '40px',
        fontSize: '16px',
        padding: '0 16px',
      },
      large: {
        height: '48px',
        fontSize: '18px',
        padding: '0 20px',
      },
    }

    const variantStyles = {
      default: {
        background: '#ffffff',
        border: `1px solid ${error ? '#ef4444' : '#d1d5db'}`,
        color: '#111827',
      },
      filled: {
        background: '#f3f4f6',
        border: `1px solid ${error ? '#ef4444' : 'transparent'}`,
        color: '#111827',
      },
      outlined: {
        background: 'transparent',
        border: `2px solid ${error ? '#ef4444' : '#d1d5db'}`,
        color: '#111827',
      },
    }

    return {
      ...baseStyles,
      ...sizeStyles[inputSize],
      ...variantStyles[variant],
    }
  }

  const getFocusStyles = () => ({
    ':focus': {
      borderColor: error ? '#ef4444' : '#4a3aff',
      boxShadow: `0 0 0 2px ${error ? '#ef4444' : '#4a3aff'}20`,
      outline: 'none',
    },
  })

  return (
    <div style={{ width: '100%' }}>
      <AntInput
        {...props}
        status={error ? 'error' : undefined}
        style={{
          ...getVariantStyles(),
          ...getFocusStyles(),
          ...style,
        }}
      />
      {helperText && (
        <div
          style={{
            marginTop: '8px',
            fontSize: '14px',
            color: error ? '#ef4444' : '#6b7280',
          }}
        >
          {helperText}
        </div>
      )}
    </div>
  )
}

const TextArea: React.FC<BrixTextAreaProps> = ({
  variant = 'default',
  error = false,
  helperText,
  style,
  rows = 4,
  ...props
}) => {
  const getVariantStyles = () => {
    const baseStyles = {
      borderRadius: '8px',
      transition: 'all 0.2s ease',
      fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
      fontSize: '16px',
      padding: '16px',
      minHeight: `${rows * 24}px`,
    }

    const variantStyles = {
      default: {
        background: '#ffffff',
        border: `1px solid ${error ? '#ef4444' : '#d1d5db'}`,
        color: '#111827',
      },
      filled: {
        background: '#f3f4f6',
        border: `1px solid ${error ? '#ef4444' : 'transparent'}`,
        color: '#111827',
      },
      outlined: {
        background: 'transparent',
        border: `2px solid ${error ? '#ef4444' : '#d1d5db'}`,
        color: '#111827',
      },
    }

    return {
      ...baseStyles,
      ...variantStyles[variant],
    }
  }

  return (
    <div style={{ width: '100%' }}>
      <AntInput.TextArea
        {...props}
        rows={rows}
        status={error ? 'error' : undefined}
        style={{
          ...getVariantStyles(),
          ...style,
        }}
      />
      {helperText && (
        <div
          style={{
            marginTop: '8px',
            fontSize: '14px',
            color: error ? '#ef4444' : '#6b7280',
          }}
        >
          {helperText}
        </div>
      )}
    </div>
  )
}

// Input.TextArea = TextArea

export default Input
export { TextArea }
export type { BrixInputProps }