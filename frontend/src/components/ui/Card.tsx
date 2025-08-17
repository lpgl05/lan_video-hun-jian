import React from 'react'
import { Card as AntCard, CardProps } from 'antd'

interface BrixCardProps extends Omit<CardProps, 'variant'> {
  variant?: 'default' | 'outlined' | 'filled'
  padding?: 'none' | 'small' | 'medium' | 'large'
  hover?: boolean
}

const Card: React.FC<BrixCardProps> = ({
  variant = 'default',
  padding = 'medium',
  hover = false,
  children,
  style,
  bodyStyle,
  headStyle,
  ...props
}) => {
  const getVariantStyles = () => {
    const baseStyles = {
      borderRadius: '12px',
      transition: 'all 0.2s ease',
      overflow: 'hidden',
    }

    const variantStyles = {
      default: {
        background: '#ffffff',
        border: '1px solid #e5e7eb',
        boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      },
      elevated: {
        background: '#ffffff',
        border: 'none',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
      },
      outlined: {
        background: '#ffffff',
        border: '2px solid #d1d5db',
        boxShadow: 'none',
      },
      filled: {
        background: '#f9fafb',
        border: '1px solid #e5e7eb',
        boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      },
    }

    const hoverStyles = hover ? {
      cursor: 'pointer',
      '&:hover': {
        transform: 'translateY(-2px)',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
      }
    } : {}

    return {
      ...baseStyles,
      ...variantStyles[variant],
      ...hoverStyles,
    }
  }

  const getPaddingStyles = () => {
    const paddingMap = {
      none: '0',
      small: '16px',
      medium: '20px',
      large: '24px',
    }
    return paddingMap[padding]
  }

  const getDefaultBodyStyle = () => ({
    padding: getPaddingStyles(),
    ...bodyStyle,
  })

  const getDefaultHeadStyle = () => ({
    background: variant === 'filled' ? '#f9fafb' : '#ffffff',
    borderBottom: '1px solid #e5e7eb',
    borderRadius: '12px 12px 0 0',
    padding: getPaddingStyles(),
    ...headStyle,
  })

  return (
    <AntCard
      {...props}
      className={`modern-card ${hover ? 'hover-card' : ''} ${props.className || ''}`}
      style={{
        ...getVariantStyles(),
        ...style,
      }}
      styles={{
        body: getDefaultBodyStyle(),
        header: props.title ? getDefaultHeadStyle() : headStyle,
      }}
    >
      {children}
    </AntCard>
  )
}

export default Card
export type { BrixCardProps }