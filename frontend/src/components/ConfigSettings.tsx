import React, { useState } from 'react'
import { Card, Input, Select, Slider, Row, Col, Space, ColorPicker, Switch, InputNumber, Button, Modal, Upload } from 'antd'
import { UploadOutlined, FontSizeOutlined } from '@ant-design/icons'
import type { DurationOption, VoiceOption, StyleConfig, FontStyle } from '../types'
import StylePreview from './StylePreview'
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
  setVideoCount
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
      label: '老报刊字体', 
      value: 'LAOBAOKAN', 
      fontUrl: 'https://picture-share-001-dpxj.oss-cn-beijing.aliyuncs.com/ziti/LAOBAOKAN.ttf',
      needsLicense: true
    },
    { 
      label: '妙笔珺俐体', 
      value: 'MiaobiJunli', 
      fontUrl: 'https://picture-share-001-dpxj.oss-cn-beijing.aliyuncs.com/%E5%A6%99%E7%AC%94%E7%8F%BA%E4%BF%90%E4%BD%93.ttf',
      needsLicense: true
    },
    { 
      label: '妙笔段慕体', 
      value: 'MiaobiDuanmu', 
      fontUrl: 'https://picture-share-001-dpxj.oss-cn-beijing.aliyuncs.com/%E5%A6%99%E7%AC%94%E6%AE%B5%E6%85%95%E4%BD%93.ttf',
      needsLicense: true
    }
  ]

  // 更新字体样式的辅助函数
  const updateFontStyle = (type: 'title' | 'subtitle', updates: Partial<FontStyle>) => {
    setStyle({
      ...style,
      [type]: { ...style[type], ...updates }
    })
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
    <div style={{ marginBottom: '12px' }}>
      <h4 style={{ marginBottom: '12px', color: '#262626', fontSize: '14px' }}>
        {label}
        <Button 
          type="link" 
          size="small" 
          icon={<FontSizeOutlined />}
          onClick={() => {
            setCurrentEditingFont(type)
            setFontModalVisible(true)
          }}
        >
          高级设置
        </Button>
      </h4>
      <Space direction="vertical" size="small" style={{ width: '100%' }}>
        {/* 基础配置 */}
        <Row gutter={12}>
          <Col span={12}>
            <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>颜色</label>
            <ColorPicker
              value={fontStyle.color}
              onChange={(color) => updateFontStyle(type, { color: color.toHexString() })}
              style={{ width: '100%' }}
            />
          </Col>
          <Col span={12}>
            <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>位置</label>
            <Select
              value={fontStyle.position}
              onChange={(position) => updateFontStyle(type, { position })}
              style={{ width: '100%' }}
              size="small"
            >
              <Select.Option value="top">顶部</Select.Option>
              <Select.Option value="center">中间</Select.Option>
              <Select.Option value="bottom">底部</Select.Option>
            </Select>
          </Col>
        </Row>
        
        <div>
          <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>
            字体大小: {fontStyle.fontSize}px
          </label>
          <Slider
            min={10}
            max={120}
            value={fontStyle.fontSize}
            onChange={(fontSize) => updateFontStyle(type, { fontSize })}
            size="small"
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>字体</label>
          <Select
            value={fontStyle.fontFamily}
            onChange={(fontFamily) => {
              const selectedFont = presetFonts.find(f => f.value === fontFamily)
              updateFontStyle(type, { 
                fontFamily,
                fontUrl: selectedFont?.fontUrl 
              })
            }}
            style={{ width: '100%' }}
            size="small"
          >
            {presetFonts.map(font => (
              <Select.Option key={font.value} value={font.value}>
                {font.label}
              </Select.Option>
            ))}
          </Select>
          {/* 版权提示 */}
          {(() => {
            const selectedFont = presetFonts.find(f => f.value === fontStyle.fontFamily)
            return selectedFont?.needsLicense && (
              <div style={{ 
                marginTop: 4, 
                fontSize: '11px', 
                color: '#999', 
                fontStyle: 'italic' 
              }}>
                该字体仅供演示，商用需联系授权
              </div>
            )
          })()}
        </div>

        {/* 描边设置 */}
        <Row gutter={8}>
          <Col span={12}>
            <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>描边颜色</label>
            <ColorPicker
              value={fontStyle.strokeColor || '#000000'}
              onChange={(color) => updateFontStyle(type, { strokeColor: color.toHexString() })}
              style={{ width: '100%' }}
            />
          </Col>
          <Col span={12}>
            <label style={{ display: 'block', marginBottom: 4, fontSize: '12px' }}>描边宽度</label>
            <InputNumber
              min={0}
              max={10}
              value={fontStyle.strokeWidth || 0}
              onChange={(strokeWidth) => updateFontStyle(type, { strokeWidth: strokeWidth || 0 })}
              style={{ width: '100%' }}
              size="small"
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
                      color: '#000000'
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
                      color: '#000000'
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
                style={{ width: '100%' }}
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
                style={{ width: '100%' }}
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

      {/* 样式预览 */}
      <StylePreview 
        titleStyle={style.title}
        subtitleStyle={style.subtitle}
        width={270}
        height={480}
      />

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
                      fontFamily: 'LAOBAOKAN',
                      fontUrl: 'https://picture-share-001-dpxj.oss-cn-beijing.aliyuncs.com/ziti/LAOBAOKAN.ttf'
                    })
                  }}
                >
                  老报刊字体
                </Button>
                <Button 
                  type="link" 
                  size="small"
                  onClick={() => {
                    updateFontStyle(currentEditingFont, {
                      fontFamily: 'MiaobiJunli',
                      fontUrl: 'https://picture-share-001-dpxj.oss-cn-beijing.aliyuncs.com/%E5%A6%99%E7%AC%94%E7%8F%BA%E4%BF%90%E4%BD%93.ttf'
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
                      fontUrl: 'https://picture-share-001-dpxj.oss-cn-beijing.aliyuncs.com/%E5%A6%99%E7%AC%94%E6%AE%B5%E6%85%95%E4%BD%93.ttf'
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