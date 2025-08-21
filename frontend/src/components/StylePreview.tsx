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

    console.log(`尝试加载字体: ${fontFamily}, URL: ${fontUrl}`)

    // 方法1: 直接尝试加载字体
    try {
      const font = new FontFace(fontFamily, `url(${fontUrl})`)
      await font.load()
      document.fonts.add(font)
      setFontsLoaded(prev => new Set([...prev, fontFamily]))
      console.log(`字体加载成功: ${fontFamily}`)
      return
    } catch (error) {
      console.error(`直接加载字体失败 ${fontFamily}:`, error)
    }

    // 方法2: 尝试使用动态CSS方式加载
    try {
      console.log(`尝试使用CSS方式加载字体: ${fontFamily}`)
      
      // 创建CSS样式
      const style = document.createElement('style')
      style.textContent = `
        @font-face {
          font-family: '${fontFamily}';
          src: url('${fontUrl}') format('truetype');
          font-display: swap;
        }
      `
      document.head.appendChild(style)
      
      // 创建一个测试元素来触发字体加载
      const testElement = document.createElement('div')
      testElement.style.fontFamily = fontFamily
      testElement.style.position = 'absolute'
      testElement.style.left = '-9999px'
      testElement.style.fontSize = '1px'
      testElement.textContent = '测试'
      document.body.appendChild(testElement)
      
      // 等待一段时间后移除测试元素
      setTimeout(() => {
        document.body.removeChild(testElement)
        setFontsLoaded(prev => new Set([...prev, fontFamily]))
        console.log(`通过CSS方式加载字体: ${fontFamily}`)
      }, 100)
      
    } catch (cssError) {
      console.error(`CSS方式加载字体也失败了:`, cssError)
      console.warn(`建议将字体文件放到项目的public文件夹中，或配置服务器CORS头部`)
    }
  }

  // 绘制视频模拟效果
  const drawVideoSimulation = (ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number) => {
    ctx.save()
    
    // 计算16:9视频区域 - 高度占背景一半
    const videoHeight = h * 0.5
    const videoWidth = videoHeight * (16 / 9)
    
    // 确保视频不超出屏幕宽度
    const actualVideoWidth = Math.min(videoWidth, w * 0.9)
    const actualVideoHeight = actualVideoWidth * (9 / 16)
    
    // 居中计算
    const videoX = x + (w - actualVideoWidth) / 2
    const videoY = y + (h - actualVideoHeight) / 2
    
    // 绘制视频区域背景
    ctx.fillStyle = 'rgba(60, 70, 80, 0.4)'
    ctx.fillRect(videoX, videoY, actualVideoWidth, actualVideoHeight)
    
    // 绘制模拟的视频场景元素（在视频区域内）
    // 1. 绘制几个模拟的人物轮廓
    ctx.fillStyle = 'rgba(100, 120, 140, 0.4)'
    
    // 人物轮廓1
    ctx.beginPath()
    ctx.ellipse(
      videoX + actualVideoWidth * 0.25, 
      videoY + actualVideoHeight * 0.4, 
      actualVideoWidth * 0.08, 
      actualVideoHeight * 0.12, 
      0, 0, Math.PI * 2
    )
    ctx.fill()
    
    // 人物轮廓2
    ctx.beginPath()
    ctx.ellipse(
      videoX + actualVideoWidth * 0.75, 
      videoY + actualVideoHeight * 0.6, 
      actualVideoWidth * 0.06, 
      actualVideoHeight * 0.1, 
      0, 0, Math.PI * 2
    )
    ctx.fill()
    
    // 2. 绘制模拟的建筑物轮廓
    ctx.fillStyle = 'rgba(80, 100, 120, 0.3)'
    
    // 建筑物1
    ctx.fillRect(
      videoX + actualVideoWidth * 0.1, 
      videoY + actualVideoHeight * 0.3, 
      actualVideoWidth * 0.15, 
      actualVideoHeight * 0.4
    )
    
    // 建筑物2
    ctx.fillRect(
      videoX + actualVideoWidth * 0.75, 
      videoY + actualVideoHeight * 0.25, 
      actualVideoWidth * 0.2, 
      actualVideoHeight * 0.5
    )
    
    // 3. 绘制一些装饰线条模拟动态效果
    ctx.strokeStyle = 'rgba(150, 170, 190, 0.2)'
    ctx.lineWidth = 1
    
    for (let i = 0; i < 5; i++) {
      ctx.beginPath()
      ctx.moveTo(
        videoX + actualVideoWidth * (0.1 + i * 0.2), 
        videoY + actualVideoHeight * 0.2
      )
      ctx.lineTo(
        videoX + actualVideoWidth * (0.15 + i * 0.2), 
        videoY + actualVideoHeight * 0.8
      )
      ctx.stroke()
    }
    
    // 4. 绘制模拟的光效
    const lightGradient = ctx.createRadialGradient(
      videoX + actualVideoWidth * 0.5, videoY + actualVideoHeight * 0.3, 0,
      videoX + actualVideoWidth * 0.5, videoY + actualVideoHeight * 0.3, actualVideoWidth * 0.3
    )
    lightGradient.addColorStop(0, 'rgba(255, 255, 255, 0.08)')
    lightGradient.addColorStop(1, 'rgba(255, 255, 255, 0)')
    
    ctx.fillStyle = lightGradient
    ctx.fillRect(videoX, videoY, actualVideoWidth, actualVideoHeight)
    
    // 5. 绘制进度条模拟播放状态
    ctx.fillStyle = 'rgba(255, 255, 255, 0.15)'
    ctx.fillRect(
      videoX + actualVideoWidth * 0.05, 
      videoY + actualVideoHeight * 0.92, 
      actualVideoWidth * 0.9, 
      2
    )
    
    ctx.fillStyle = 'rgba(24, 144, 255, 0.9)'
    ctx.fillRect(
      videoX + actualVideoWidth * 0.05, 
      videoY + actualVideoHeight * 0.92, 
      actualVideoWidth * 0.4, 
      2
    )
    
    // 6. 绘制播放按钮
    const playButtonSize = Math.min(actualVideoWidth, actualVideoHeight) * 0.15
    const playButtonX = videoX + actualVideoWidth / 2
    const playButtonY = videoY + actualVideoHeight / 2
    
    // 播放按钮背景圆形
    ctx.fillStyle = 'rgba(240, 240, 240, 0.8)'
    ctx.beginPath()
    ctx.arc(playButtonX, playButtonY, playButtonSize, 0, Math.PI * 2)
    ctx.fill()
    
    // 播放按钮边框
    ctx.strokeStyle = 'rgba(200, 200, 200, 0.9)'
    ctx.lineWidth = 2
    ctx.stroke()
    
    // 播放三角形
    ctx.fillStyle = 'rgba(100, 100, 100, 0.9)'
    ctx.beginPath()
    const triangleSize = playButtonSize * 0.4
    ctx.moveTo(playButtonX - triangleSize * 0.3, playButtonY - triangleSize * 0.6)
    ctx.lineTo(playButtonX - triangleSize * 0.3, playButtonY + triangleSize * 0.6)
    ctx.lineTo(playButtonX + triangleSize * 0.7, playButtonY)
    ctx.closePath()
    ctx.fill()
    
    // 7. 绘制"案例视频"标签
    ctx.fillStyle = 'rgba(50, 50, 50, 0.8)'
    ctx.fillRect(
      videoX + actualVideoWidth * 0.02,
      videoY + actualVideoHeight * 0.02,
      actualVideoWidth * 0.25,
      actualVideoHeight * 0.08
    )
    
    // 标签文字
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)'
    ctx.font = `${Math.max(10, actualVideoWidth * 0.03)}px Microsoft YaHei, sans-serif`
    ctx.textAlign = 'center'
    ctx.fillText(
      '案例视频',
      videoX + actualVideoWidth * 0.145,
      videoY + actualVideoHeight * 0.065
    )
    
    ctx.restore()
  }

  // 绘制手机壳
  const drawPhoneFrame = (ctx: CanvasRenderingContext2D) => {
    const frameThickness = 12
    const cornerRadius = 25
    const screenPadding = 8
    
    // 绘制手机外壳
    ctx.save()
    
    // 外壳渐变色
    const frameGradient = ctx.createLinearGradient(0, 0, width, height)
    frameGradient.addColorStop(0, '#1a1a1a')
    frameGradient.addColorStop(0.5, '#2a2a2a')
    frameGradient.addColorStop(1, '#1a1a1a')
    
    // 绘制圆角矩形外壳
    ctx.fillStyle = frameGradient
    ctx.beginPath()
    ctx.roundRect(0, 0, width, height, cornerRadius)
    ctx.fill()
    
    // 绘制内部屏幕区域（挖空效果）
    ctx.globalCompositeOperation = 'destination-out'
    ctx.beginPath()
    ctx.roundRect(
      frameThickness, 
      frameThickness + 20, 
      width - frameThickness * 2, 
      height - frameThickness * 2 - 40, 
      cornerRadius - 8
    )
    ctx.fill()
    
    ctx.restore()
    
    // 绘制听筒
    ctx.fillStyle = '#333'
    ctx.beginPath()
    ctx.roundRect(width / 2 - 25, 8, 50, 4, 2)
    ctx.fill()
    
    // 绘制前置摄像头
    ctx.fillStyle = '#111'
    ctx.beginPath()
    ctx.arc(width / 2 + 40, 12, 3, 0, Math.PI * 2)
    ctx.fill()
    
    // 绘制底部home指示器
    ctx.fillStyle = '#444'
    ctx.beginPath()
    ctx.roundRect(width / 2 - 30, height - 12, 60, 3, 2)
    ctx.fill()
  }

  // 绘制预览
  const drawPreview = () => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // 清空画布
    ctx.clearRect(0, 0, width, height)
    
    // 绘制手机壳
    drawPhoneFrame(ctx)

    // 计算屏幕内容区域
    const screenX = 12
    const screenY = 32
    const screenWidth = width - 24
    const screenHeight = height - 64

    // 设置裁剪区域为屏幕内部
    ctx.save()
    ctx.beginPath()
    ctx.roundRect(screenX, screenY, screenWidth, screenHeight, 17)
    ctx.clip()

    // 绘制背景（深灰色渐变模拟视频背景）
    const gradient = ctx.createLinearGradient(screenX, screenY, screenX + screenWidth, screenY + screenHeight)
    gradient.addColorStop(0, '#404040')
    gradient.addColorStop(1, '#2a2a2a')
    ctx.fillStyle = gradient
    ctx.fillRect(screenX, screenY, screenWidth, screenHeight)

    // 添加视频模拟效果
    drawVideoSimulation(ctx, screenX, screenY, screenWidth, screenHeight)

    // 绘制标题
    drawText(ctx, '示例标题文本', titleStyle, screenWidth, screenHeight, 'title', screenX, screenY)

    // 绘制字幕
    drawText(ctx, '示例字幕文本', subtitleStyle, screenWidth, screenHeight, 'subtitle', screenX, screenY)
    
    ctx.restore()
  }

  // 绘制文本的函数
  const drawText = (
    ctx: CanvasRenderingContext2D,
    text: string,
    style: FontStyle,
    canvasWidth: number,
    canvasHeight: number,
    type: 'title' | 'subtitle',
    offsetX: number = 0,
    offsetY: number = 0
  ) => {
    // 修正：实际视频尺寸为1080x1920(竖屏)，但后端按1080宽度处理
    const actualVideoWidth = 1080  // 后端实际使用的视频宽度
    const previewVideoHeight = canvasHeight * 0.5 // 视频高度占画布一半
    const previewVideoWidth = previewVideoHeight * (16 / 9)
    
    // 确保不超出画布宽度
    const actualPreviewWidth = Math.min(previewVideoWidth, canvasWidth * 0.9)
    
    // 计算字体缩放比例（基于宽度比例，因为后端以宽度为准）
    const fontScale = actualPreviewWidth / actualVideoWidth
    const scaledFontSize = Math.max(6, style.fontSize * fontScale) // 最小字体6px
    
    // 设置字体
    let fontFamily = style.fontFamily
    
    // 检查是否是自定义字体并且已加载
    if (style.fontUrl && fontsLoaded.has(style.fontFamily)) {
      console.log(`使用已加载的自定义字体: ${style.fontFamily}`)
    } else if (style.fontUrl && !fontsLoaded.has(style.fontFamily)) {
      console.warn(`自定义字体 ${style.fontFamily} 尚未加载，使用默认字体`)
      fontFamily = 'Microsoft YaHei, sans-serif' // 备用字体
    }
    
    let fontString = `${scaledFontSize}px "${fontFamily}"`
    if (style.bold) fontString = `bold ${fontString}`
    if (style.italic) fontString = `italic ${fontString}`
    ctx.font = fontString
    
    console.log(`设置字体: ${fontString}`)

    // 计算文本位置
    const textMetrics = ctx.measureText(text)
    const textWidth = textMetrics.width
    const textHeight = scaledFontSize
    
    let x = offsetX + (canvasWidth - textWidth) / 2 // 水平居中，加上偏移
    let y: number

    // 根据位置设置Y坐标
    switch (style.position) {
      case 'top':
        y = offsetY + (type === 'title' ? textHeight + 20 : textHeight + 60)
        break
      case 'center':
        y = offsetY + canvasHeight / 2 + (type === 'title' ? -textHeight : textHeight)
        break
      case 'bottom':
        y = offsetY + canvasHeight - (type === 'title' ? textHeight + 60 : textHeight + 20)
        break
      default:
        y = offsetY + canvasHeight / 2
    }

    // 绘制描边
    if (style.strokeColor && style.strokeWidth && style.strokeWidth > 0) {
      ctx.strokeStyle = style.strokeColor
      const scaledStrokeWidth = Math.max(0.5, style.strokeWidth * fontScale) // 缩放描边宽度
      ctx.lineWidth = scaledStrokeWidth * 2 // Canvas描边是双向的，所以乘以2
      ctx.lineJoin = 'round'
      ctx.miterLimit = 2
      ctx.strokeText(text, x, y)
    }

    // 绘制阴影
    if (style.shadow && style.shadowColor) {
      ctx.save()
      ctx.shadowColor = style.shadowColor
      ctx.shadowBlur = Math.max(1, 4 * fontScale) // 缩放阴影模糊
      ctx.shadowOffsetX = Math.max(0.5, 2 * fontScale) // 缩放阴影偏移
      ctx.shadowOffsetY = Math.max(0.5, 2 * fontScale)
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
      <div style={{ display: 'flex', justifyContent: 'center', padding: '8px' }}>
        <canvas
          ref={canvasRef}
          width={width}
          height={height}
          style={{
            borderRadius: '25px',
            backgroundColor: 'transparent',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)'
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
        <br />
        <span style={{ fontSize: '11px', color: '#999' }}>
          字体已按比例缩放至预览尺寸
        </span>
      </div>
    </Card>
  )
}

export default StylePreview
