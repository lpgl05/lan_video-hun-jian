import React from 'react'
import { Select as AntSelect, SelectProps } from 'antd'
import { DownOutlined } from '@ant-design/icons'

interface BrixSelectProps extends Omit<SelectProps, 'variant'> {
  variant?: 'default' | 'filled' | 'outlined'
  selectSize?: 'small' | 'medium' | 'large'
  error?: boolean
  helperText?: string
}

const Select: React.FC<BrixSelectProps> = ({
  variant = 'default',
  selectSize = 'medium',
  error = false,
  helperText,
  style,
  dropdownStyle,
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
      },
      medium: {
        height: '40px',
        fontSize: '16px',
      },
      large: {
        height: '48px',
        fontSize: '18px',
      },
    }

    const variantStyles = {
      default: {
        background: '#ffffff',
        borderColor: error ? '#ef4444' : '#d1d5db',
        color: '#111827',
      },
      filled: {
        background: '#f3f4f6',
        borderColor: error ? '#ef4444' : 'transparent',
        color: '#111827',
      },
      outlined: {
        background: 'transparent',
        borderColor: error ? '#ef4444' : '#d1d5db',
        borderWidth: '2px',
        color: '#111827',
      },
    }

    return {
      ...baseStyles,
      ...sizeStyles[selectSize],
      ...variantStyles[variant],
    }
  }

  const getDropdownStyles = () => ({
    background: '#ffffff',
    borderRadius: '8px',
    border: '1px solid #e5e7eb',
    boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    padding: '8px',
    ...dropdownStyle,
  })

  return (
    <div style={{ width: '100%' }}>
      <AntSelect
        {...props}
        status={error ? 'error' : undefined}
        suffixIcon={<DownOutlined style={{ color: '#6b7280' }} />}
        style={{
          width: '100%',
          ...getVariantStyles(),
          ...style,
        }}
        popupMatchSelectWidth={false}
        styles={{
          dropdown: getDropdownStyles(),
        }}
        className="brix-select-dropdown"
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

export default Select
export type { BrixSelectProps }