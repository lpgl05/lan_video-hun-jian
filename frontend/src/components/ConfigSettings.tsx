import React, { useState, useEffect } from 'react'
import { Card, Input, Select, Slider, Row, Col, Space, ColorPicker, Switch, InputNumber, Button, Modal, Upload } from 'antd'
import { UploadOutlined, FontSizeOutlined } from '@ant-design/icons'
import type { DurationOption, VoiceOption, StyleConfig, FontStyle, PosterFile } from '../types'
import StylePreview from './StylePreview'
import PosterUpload from './PosterUpload'
import '../styles/FontStyles.css'

interface ConfigSettingsProps {
  duration: DurationOption
  setDuration: (duration: DurationOption) => void
  voice: VoiceOption
  setVoice: (voice: VoiceOption) => void
  style: StyleConfig
  setStyle: (style: StyleConfig) => void
  projectName?: string
  setProjectName?: (name: string) => void
  videoCount?: number
  setVideoCount?: (count: number) => void
  posters?: PosterFile[] // 海报数组
  setPosters?: (posters: PosterFile[]) => void // 海报设置函数
}

const ConfigSettings: React.FC<ConfigSettingsProps> = ({
  duration,
  setDuration,
  voice,
  setVoice,
  style,
  setStyle,
  projectName,
  setProjectName,
  videoCount,
  setVideoCount,
  posters,
  setPosters
}) => {
  const [fontModalVisible, setFontModalVisible] = useState(false)
  const [currentEditingFont, setCurrentEditingFont] = useState<'title' | 'subtitle'>('title')

  // 预设字体选项
  const presetFonts = [
    { label: '系统默认', value: 'Arial, sans-serif', needsLicense: false },
    { label: '微软雅黑', value: 'Microsoft YaHei, sans-serif', needsLicense: false },
    { label: '宋体', value: 'SimSun, serif', needsLicense: false },
    { label: '黑体', value: 'SimHei, sans-serif', needsLicense: false },
    { label: '楷体', value: 'KaiTi, serif', needsLicense: false },
    { 
      label: '柳隶宋体', 
      value: 'LIULISONG', 
      fontUrl: '/fonts/LIULISONG.ttf',
      needsLicense: true
    },
    { 
      label: '妙笔珺俐体', 
      value: 'MiaobiJunli', 
      fontUrl: '/fonts/妙笔珺俐体.ttf',
      needsLicense: true
    },
    { 
      label: '妙笔段慕体', 
      value: 'MiaobiDuanmu', 
      fontUrl: '/fonts/妙笔段慕体.ttf',
      needsLicense: true
    },
    { 
      label: '思源黑体Heavy', 
      value: 'SourceHanSansCN-Heavy', 
      fontUrl: '/fonts/SourceHanSansCN-Heavy.otf',
      needsLicense: true
    }
  ]

  // 在组件加载时应用默认值
  useEffect(() => {
    // 确保当前style应用了所有默认值
    const normalized = normalizeStyle(style)
    if (JSON.stringify(normalized) !== JSON.stringify(style)) {
      setStyle(normalized)
    }
  }, []) // 只在组件首次加载时执行

  // 新增：统一规范化 style，确保 title/subtitle 都有 background/background_color/background_opacity
  const normalizeStyle = (rawStyle: any) => {
    const s = { ...(rawStyle || {}) }
    const ensureSection = (key: 'title' | 'subtitle') => {
      const sec = (s[key] && { ...s[key] }) || {}
      const bgObj = (sec.background && typeof sec.background === 'object') ? { ...sec.background } : {}
      if (!bgObj.background_color && sec.background_color) bgObj.background_color = sec.background_color
      if (bgObj.background_opacity === undefined && sec.background_opacity !== undefined) bgObj.background_opacity = sec.background_opacity
      if (bgObj.opacity === undefined && sec.opacity !== undefined) bgObj.background_opacity = sec.opacity
      if (!bgObj.background_color) bgObj.background_color = (key === 'title') ? '#CEC970' : '#FFFFFF'
      if (bgObj.background_opacity === undefined) bgObj.background_opacity = 0  // 默认背景透明度为0
      sec.background = bgObj
      sec.background_color = sec.background_color || bgObj.background_color
      sec.background_opacity = sec.background_opacity ?? bgObj.background_opacity
      sec.color = sec.color || (key === 'title' ? '#000' : '#ffffff')
      sec.position = sec.position || (key === 'title' ? 'top' : 'template1')  // 字幕默认为template1位置
      sec.fontSize = sec.fontSize ?? (key === 'title' ? 0 : 60)  // 标题默认字体大小为0
      sec.fontFamily = sec.fontFamily || 'SourceHanSansCN-Heavy'  // 默认字体为思源黑体Heavy
      s[key] = sec
    }
    ensureSection('title')
    ensureSection('subtitle')
    return s
  }

  // 更新字体样式的辅助函数（增强：规范 background 字段，保持兼容）
  const updateFontStyle = (type: 'title' | 'subtitle', updates: Partial<FontStyle>) => {
		const prev = (style && style[type]) || {}
		const merged: any = { ...prev, ...updates }

		// 处理 background 字段优先级：支持 object/string/flat fields
		if (merged.background) {
			const bg = merged.background
			if (typeof bg === 'string') {
				merged.background_color = merged.background_color || bg
			} else if (typeof bg === 'object') {
				if (bg.background_color) merged.background_color = bg.background_color
				if (bg.background_opacity !== undefined) merged.background_opacity = bg.background_opacity
				if (bg.color) merged.background_color = merged.background_color || bg.color
				if (bg.opacity !== undefined) merged.background_opacity = merged.background_opacity ?? bg.opacity
			}
		}

		// 如果设置了平铺字段，确保 background 对象也同步存在
		if ((merged.background_color || merged.background_opacity !== undefined) && !merged.background) {
			merged.background = {
				// 标题缺省颜色改为 #cec970，字幕仍然默认 #000000
				background_color: merged.background_color || (type === 'title' ? '#cec970' : '#000000'),
				background_opacity: merged.background_opacity !== undefined ? merged.background_opacity : 0
			}
		} else if (merged.background && (!merged.background.background_color && merged.background_color)) {
			merged.background.background_color = merged.background_color
			merged.background.background_opacity = merged.background_opacity ?? merged.background.background_opacity
		}

		// 先合并到现有 style，然后规范化整个 style（保证 title/subtitle 都有 background）
		const newStyle = {
			...style,
			[type]: merged
		}
		setStyle(normalizeStyle(newStyle))
	}

	// 新增：获取当前 background（若无则返回空对象）
	const getCurrentBackground = (type: 'title' | 'subtitle') => {
		return (style && style[type] && (style[type] as any).background) ? (style[type] as any).background : {}
	}

  // 处理自定义字体上传
  const handleFontUpload = (file: File) => {
    const url = URL.createObjectURL(file)
    const fontName = file.name.replace(/\.(ttf|otf|woff|woff2)$/i, '')
    
    updateFontStyle(currentEditingFont, {
      fontFamily: fontName,
      fontUrl: url
    })
    
    return false // 阻止默认上传行为
  }

  // 渲染字体样式配置
  const renderFontStyleConfig = (type: 'title' | 'subtitle', label: string, fontStyle: FontStyle) => (
    <div style={{ 
      padding: '12px', 
      border: `2px solid ${type === 'title' ? '#1890ff' : '#52c41a'}`, 
      borderRadius: '8px',
      backgroundColor: type === 'title' ? '#f0f8ff' : '#f6ffed',
      marginBottom: '12px'
    }}>
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        marginBottom: '12px'
      }}>
        <h4 style={{ 
          margin: 0, 
          fontSize: '14px', 
          fontWeight: 600,
          color: type === 'title' ? '#1890ff' : '#52c41a',
          display: 'flex',
          alignItems: 'center',
          gap: '4px'
        }}>
          <FontSizeOutlined /> {label}
        </h4>
        <Button 
          type="link" 
          size="small" 
          onClick={() => {
            setCurrentEditingFont(type)
            setFontModalVisible(true)
          }}
          style={{ fontSize: '12px', height: 'auto', padding: '2px 8px' }}
        >
          高级设置
        </Button>
      </div>
      <Space direction="vertical" size="small" style={{ width: '100%' }}>
        {/* 基础配置 */}
        <Row gutter={12}>
          <Col span={12}>
            <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>
              {type === 'title' ? '标题颜色' : '字幕颜色'}
            </label>
            <ColorPicker
              value={fontStyle.color}
              onChange={(color) => updateFontStyle(type, { color: color.toHexString() })}
              showText
              style={{ width: '100%', height: '32px' }}
            />
          </Col>
          <Col span={12}>
            <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>
              {type === 'title' ? '标题位置' : '字幕位置'}
            </label>
            <Select
              value={fontStyle.position}
              onChange={(position) => updateFontStyle(type, { position })}
              style={{ width: '100%', height: '32px' }}
            >
              <Select.Option value="top">顶部</Select.Option>
              <Select.Option value="center">中间</Select.Option>
              <Select.Option value="bottom">底部</Select.Option>
              <Select.Option value="template1">模板位置1（横屏视频）</Select.Option>
            </Select>
          </Col>
        </Row>
        
        {/* 第二行：字体大小和字体 */}
        <Row gutter={12}>
          <Col span={8}>
            <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>字体大小</label>
            <InputNumber
              min={0}
              max={type === 'title' ? 200 : 120}
              value={fontStyle.fontSize}
              onChange={(fontSize) => updateFontStyle(type, { fontSize: fontSize || 0 })}
              style={{ width: '100%', height: '32px', lineHeight: '30px' }}
              addonAfter="px"
              placeholder="0=不显示"
            />
          </Col>
          <Col span={16}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: 4 }}>
              <label style={{ fontSize: '12px', marginRight: 8 }}>字体</label>
              {/* 版权提示放在标题后面 */}
              {(() => {
                const selectedFont = presetFonts.find(f => f.value === fontStyle.fontFamily)
                return selectedFont?.needsLicense && (
                  <span style={{ 
                    fontSize: '10px', 
                    color: '#ff4d4f',
                    fontStyle: 'italic',
                    marginLeft: 'auto'
                  }}>
                    该字体仅供演示，商用需联系授权
                  </span>
                )
              })()}
            </div>
            <Select
              value={fontStyle.fontFamily}
              onChange={(fontFamily) => {
                const selectedFont = presetFonts.find(f => f.value === fontFamily)
                updateFontStyle(type, { 
                  fontFamily,
                  fontUrl: selectedFont?.fontUrl || undefined
                })
              }}
              style={{ width: '100%', height: '32px' }}
            >
              {presetFonts.map(font => (
                <Select.Option key={font.value} value={font.value}>
                  {font.label}
                </Select.Option>
              ))}
            </Select>
          </Col>
        </Row>

        {/* 第三行：描边设置 */}
        <Row gutter={12}>
          <Col span={12}>
            <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>字体描边颜色</label>
            <ColorPicker
              value={fontStyle.strokeColor || '#000000'}
              onChange={(color) => updateFontStyle(type, { strokeColor: color.toHexString() })}
              showText
              style={{ width: '100%', height: '32px' }}
            />
          </Col>
          <Col span={12}>
            <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>字体描边宽度</label>
            <InputNumber
              min={0}
              max={10}
              value={fontStyle.strokeWidth || 1}
              onChange={(strokeWidth) => updateFontStyle(type, { strokeWidth: strokeWidth || 0 })}
              style={{ width: '100%', height: '32px', lineHeight: '30px' }}
              addonAfter="px"
            />
          </Col>
        </Row>

        {/* 新增：背景颜色与透明度设置 */}
        <Row gutter={12} style={{ marginTop: 8 }}>
          <Col span={12}>
            <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>{type === 'title' ? '标题背景颜色' : '字幕背景颜色'}</label>
            <ColorPicker
              value={ (getCurrentBackground(type).background_color) || (type === 'title' ? '#CEC970' : '#FFFFFF') }
              onChange={(color) => {
                const curBg = getCurrentBackground(type)
                const newBg = { ...curBg, background_color: color.toHexString() }
                updateFontStyle(type, { background: newBg } as any)
              }}
              showText
              style={{ width: '100%', height: '32px' }}
            />
          </Col>
          <Col span={12}>
            <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>{type === 'title' ? '标题背景透明度' : '字幕背景透明度'}</label>
            <InputNumber
              min={0}
              max={255}
              value={ getCurrentBackground(type).background_opacity ?? getCurrentBackground(type).opacity ?? 0 }
              onChange={(val) => {
                const curBg = getCurrentBackground(type)
                let opacity = typeof val === 'number' ? val : parseFloat(String(val) || '0')
                if (opacity <= 1) opacity = Math.round(opacity * 255)
                const newBg = { ...curBg, background_opacity: Math.round(opacity) }
                updateFontStyle(type, { background: newBg } as any)
              }}
              style={{ width: '100%', height: '32px' }}
            />
          </Col>
        </Row>
      </Space>
    </div>
  )
  return (
    <Space direction="vertical" size="middle" style={{ width: '100%' }}>
      {/* 基础配置 */}
      <Card title="基础设置" size="small">
        <Row gutter={[16, 12]}>
          {/* 项目名称和视频生成数量 */}
          {(projectName !== undefined && setProjectName) && (
            <>
              <Col span={12}>
                <div>
                  <label style={{ display: 'block', marginBottom: 8 }}>项目名称</label>
                  <Input
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    placeholder="请输入项目名称"
                    style={{
                      backgroundColor: '#ffffff',
                      color: '#000000',
                      height: '32px'
                    }}
                  />
                </div>
              </Col>
              <Col span={12}>
                <div>
                  <label style={{ display: 'block', marginBottom: 8 }}>视频生成数量</label>
                  <Input
                    type="number"
                    min={1}
                    max={10}
                    value={videoCount}
                    onChange={(e) => setVideoCount && setVideoCount(parseInt(e.target.value) || 1)}
                    style={{
                      backgroundColor: '#ffffff',
                      color: '#000000',
                      height: '32px'
                    }}
                  />
                </div>
              </Col>
            </>
          )}
          
          <Col span={12}>
            <div>
              <label style={{ display: 'block', marginBottom: 8 }}>视频时长</label>
              <Select
                value={duration}
                onChange={setDuration}
                style={{ width: '100%', height: '32px' }}
              >
                <Select.Option value="30s">30秒</Select.Option>
                <Select.Option value="60s">60秒</Select.Option>
                <Select.Option value="90s">90秒</Select.Option>
              </Select>
            </div>
          </Col>
          <Col span={12}>
            <div>
              <label style={{ display: 'block', marginBottom: 8 }}>配音类型</label>
              <Select
                value={voice}
                onChange={setVoice}
                style={{ width: '100%', height: '32px' }}
              >
                <Select.Option value="male">男声</Select.Option>
                <Select.Option value="female">女声</Select.Option>
              </Select>
            </div>
          </Col>
        </Row>
      </Card>

      {/* 样式配置 */}
      <Card title="样式设置" size="small">
        <Row gutter={[16, 12]}>
          <Col span={12}>
            {renderFontStyleConfig('title', '标题样式', style.title)}
          </Col>
          
          <Col span={12}>
            {renderFontStyleConfig('subtitle', '字幕样式', style.subtitle)}
          </Col>
        </Row>
      </Card>

      {/* 海报背景设置 */}
      {setPosters && (
        <Card title="背景海报设置" size="small">
          <PosterUpload 
            posters={posters || []}
            onPostersChange={setPosters}
          />
        </Card>
      )}

      {/* 样式预览 */}
      {(() => {
        const posterUrl = posters && posters.length > 0 ? posters[0].url : undefined
        console.log('ConfigSettings - posters:', posters)
        console.log('ConfigSettings - posterUrl:', posterUrl)
        return (
          <StylePreview 
            titleStyle={style.title}
            subtitleStyle={style.subtitle}
            width={270}
            height={480}
            posterUrl={posterUrl}
          />
        )
      })()}

      {/* 高级字体设置模态框 */}
      <Modal
        title={`${currentEditingFont === 'title' ? '标题' : '字幕'}高级字体设置`}
        open={fontModalVisible}
        onCancel={() => setFontModalVisible(false)}
        footer={[
          <Button key="cancel" onClick={() => setFontModalVisible(false)}>
            关闭
          </Button>
        ]}
        width={600}
      >
        <Space direction="vertical" size="middle" style={{ width: '100%' }}>
          {/* 字体样式选项 */}
          <Card title="字体样式" size="small">
            <Row gutter={16}>
              <Col span={8}>
                <label style={{ display: 'block', marginBottom: 8 }}>加粗</label>
                <Switch
                  checked={style[currentEditingFont].bold || false}
                  onChange={(bold) => updateFontStyle(currentEditingFont, { bold })}
                />
              </Col>
              <Col span={8}>
                <label style={{ display: 'block', marginBottom: 8 }}>斜体</label>
                <Switch
                  checked={style[currentEditingFont].italic || false}
                  onChange={(italic) => updateFontStyle(currentEditingFont, { italic })}
                />
              </Col>
              <Col span={8}>
                <label style={{ display: 'block', marginBottom: 8 }}>阴影</label>
                <Switch
                  checked={style[currentEditingFont].shadow || false}
                  onChange={(shadow) => updateFontStyle(currentEditingFont, { shadow })}
                />
              </Col>
            </Row>
          </Card>

          {/* 阴影设置 */}
          {style[currentEditingFont].shadow && (
            <Card title="阴影设置" size="small">
              <label style={{ display: 'block', marginBottom: 8 }}>阴影颜色</label>
              <ColorPicker
                value={style[currentEditingFont].shadowColor || '#000000'}
                onChange={(color) => updateFontStyle(currentEditingFont, { shadowColor: color.toHexString() })}
              />
            </Card>
          )}

          {/* 自定义字体上传 */}
          <Card title="自定义字体" size="small">
            <Upload
              beforeUpload={handleFontUpload}
              accept=".ttf,.otf,.woff,.woff2"
              showUploadList={false}
            >
              <Button icon={<UploadOutlined />}>
                上传字体文件 (TTF/OTF/WOFF)
              </Button>
            </Upload>
            <div style={{ marginTop: 8, fontSize: '12px', color: '#666' }}>
              当前字体: {style[currentEditingFont].fontFamily}
            </div>
          </Card>

          {/* 字体URL输入 */}
          <Card title="字体链接" size="small">
            <Input
              placeholder="输入字体文件URL (如: https://example.com/font.ttf)"
              value={style[currentEditingFont].fontUrl || ''}
              onChange={(e) => {
                const fontUrl = e.target.value
                const fontName = fontUrl.split('/').pop()?.replace(/\.(ttf|otf|woff|woff2)$/i, '') || 'CustomFont'
                updateFontStyle(currentEditingFont, { 
                  fontUrl,
                  fontFamily: fontName
                })
              }}
            />
            <div style={{ marginTop: 8, fontSize: '12px', color: '#666' }}>
              <div style={{ marginBottom: 8 }}>推荐字体：</div>
              <Space wrap>
                <Button 
                  type="link" 
                  size="small"
                  onClick={() => {
                    updateFontStyle(currentEditingFont, {
                      fontFamily: 'LIULISONG',
                      fontUrl: '/fonts/LIULISONG.ttf'
                    })
                  }}
                >
                  柳隶宋体
                </Button>
                <Button 
                  type="link" 
                  size="small"
                  onClick={() => {
                    updateFontStyle(currentEditingFont, {
                      fontFamily: 'MiaobiJunli',
                      fontUrl: '/fonts/妙笔珺俐体.ttf'
                    })
                  }}
                >
                  妙笔珺俐体
                </Button>
                <Button 
                  type="link" 
                  size="small"
                  onClick={() => {
                    updateFontStyle(currentEditingFont, {
                      fontFamily: 'MiaobiDuanmu',
                      fontUrl: '/fonts/妙笔段慕体.ttf'
                    })
                  }}
                >
                  妙笔段慕体
                </Button>
              </Space>
              <div style={{ marginTop: 4, fontSize: '11px', color: '#999', fontStyle: 'italic' }}>
                以上字体仅供演示，商用需联系授权
              </div>
            </div>
          </Card>
        </Space>
      </Modal>
    </Space>
  )
}

export default ConfigSettings