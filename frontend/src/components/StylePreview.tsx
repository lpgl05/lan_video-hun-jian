import React, { useRef, useEffect, useState } from 'react'
import { Card } from 'antd'
import type { FontStyle } from '../types'

interface StylePreviewProps {
  titleStyle: FontStyle
  subtitleStyle: FontStyle
  width?: number
  height?: number
}

const StylePreview: React.FC<StylePreviewProps> = ({
  titleStyle,
  subtitleStyle,
  width = 270,
  height = 480
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [fontsLoaded, setFontsLoaded] = useState<Set<string>>(new Set())

  // 加载自定义字体
  const loadFont = async (fontFamily: string, fontUrl?: string) => {
    if (!fontUrl || fontsLoaded.has(fontFamily)) return

    try {
      const font = new FontFace(fontFamily, `url(${fontUrl})`)
      await font.load()
      document.fonts.add(font)
      setFontsLoaded(prev => new Set([...prev, fontFamily]))
    } catch (error) {
      console.warn(`Failed to load font ${fontFamily}:`, error)
    }
  }

  // 绘制预览
  const drawPreview = () => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // 清空画布
    ctx.clearRect(0, 0, width, height)

    // 绘制背景（深灰色渐变模拟视频背景）
    const gradient = ctx.createLinearGradient(0, 0, width, height)
    gradient.addColorStop(0, '#404040')
    gradient.addColorStop(1, '#2a2a2a')
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, width, height)

    // 绘制标题
    drawText(ctx, '示例标题文本', titleStyle, width, height, 'title')

    // 绘制字幕
    drawText(ctx, '示例字幕文本', subtitleStyle, width, height, 'subtitle')
  }

  // 绘制文本的函数
  const drawText = (
    ctx: CanvasRenderingContext2D,
    text: string,
    style: FontStyle,
    canvasWidth: number,
    canvasHeight: number,
    type: 'title' | 'subtitle'
  ) => {
    // 设置字体
    let fontString = `${style.fontSize}px ${style.fontFamily}`
    if (style.bold) fontString = `bold ${fontString}`
    if (style.italic) fontString = `italic ${fontString}`
    ctx.font = fontString

    // 计算文本位置
    const textMetrics = ctx.measureText(text)
    const textWidth = textMetrics.width
    const textHeight = style.fontSize
    
    let x = (canvasWidth - textWidth) / 2 // 水平居中
    let y: number

    // 根据位置设置Y坐标
    switch (style.position) {
      case 'top':
        y = type === 'title' ? textHeight + 20 : textHeight + 60
        break
      case 'center':
        y = canvasHeight / 2 + (type === 'title' ? -textHeight : textHeight)
        break
      case 'bottom':
        y = canvasHeight - (type === 'title' ? textHeight + 60 : textHeight + 20)
        break
      default:
        y = canvasHeight / 2
    }

    // 绘制描边
    if (style.strokeColor && style.strokeWidth && style.strokeWidth > 0) {
      ctx.strokeStyle = style.strokeColor
      ctx.lineWidth = style.strokeWidth * 2 // Canvas描边是双向的，所以乘以2
      ctx.lineJoin = 'round'
      ctx.miterLimit = 2
      ctx.strokeText(text, x, y)
    }

    // 绘制阴影
    if (style.shadow && style.shadowColor) {
      ctx.save()
      ctx.shadowColor = style.shadowColor
      ctx.shadowBlur = 4
      ctx.shadowOffsetX = 2
      ctx.shadowOffsetY = 2
      ctx.fillStyle = style.color
      ctx.fillText(text, x, y)
      ctx.restore()
    } else {
      // 绘制主文本
      ctx.fillStyle = style.color
      ctx.fillText(text, x, y)
    }
  }

  // 当样式改变时重新绘制
  useEffect(() => {
    const loadFonts = async () => {
      await Promise.all([
        loadFont(titleStyle.fontFamily, titleStyle.fontUrl),
        loadFont(subtitleStyle.fontFamily, subtitleStyle.fontUrl)
      ])
      // 延迟一下确保字体加载完成
      setTimeout(drawPreview, 100)
    }

    loadFonts()
  }, [titleStyle, subtitleStyle, width, height, fontsLoaded])

  return (
    <Card title="样式预览" size="small" style={{ marginTop: 16 }}>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <canvas
          ref={canvasRef}
          width={width}
          height={height}
          style={{
            border: '1px solid #d9d9d9',
            borderRadius: '8px',
            backgroundColor: '#fafafa'
          }}
        />
      </div>
      <div style={{ 
        marginTop: 8, 
        fontSize: '12px', 
        color: '#666', 
        textAlign: 'center' 
      }}>
        预览效果 ({width} × {height})
      </div>
    </Card>
  )
}

export default StylePreview
