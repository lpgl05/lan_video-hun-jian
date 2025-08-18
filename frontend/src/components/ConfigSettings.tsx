import React from 'react'
import { Card, Input, Select, Slider, Row, Col, Space, ColorPicker } from 'antd'
import type { DurationOption, VoiceOption, StyleConfig } from '../types'

interface ConfigSettingsProps {
  duration: DurationOption
  setDuration: (duration: DurationOption) => void
  voice: VoiceOption
  setVoice: (voice: VoiceOption) => void
  style: StyleConfig
  setStyle: (style: StyleConfig) => void
}

const ConfigSettings: React.FC<ConfigSettingsProps> = ({
  duration,
  setDuration,
  voice,
  setVoice,
  style,
  setStyle
}) => {
  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      {/* 基础配置 */}
      <Card title="基础设置" size="small">
        <Row gutter={[16, 16]}>
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
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <div style={{ marginBottom: '16px' }}>
              <h4 style={{ marginBottom: '12px', color: '#262626' }}>主标题样式</h4>
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <label style={{ display: 'block', marginBottom: 8 }}>颜色</label>
                  <ColorPicker
                    value={style.title.color}
                    onChange={(color) => 
                      setStyle({
                        ...style,
                        title: { ...style.title, color: color.toHexString() }
                      })
                    }
                  />
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: 8 }}>位置</label>
                  <Select
                    value={style.title.position}
                    onChange={(position) =>
                      setStyle({
                        ...style,
                        title: { ...style.title, position }
                      })
                    }
                    style={{ width: '100%' }}
                  >
                    <Select.Option value="top">顶部</Select.Option>
                    <Select.Option value="center">中间</Select.Option>
                    <Select.Option value="bottom">底部</Select.Option>
                  </Select>
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: 8 }}>
                    字体大小: {style.title.fontSize}px
                  </label>
                  <Slider
                    min={10}
                    max={120}
                    value={style.title.fontSize}
                    onChange={(fontSize) =>
                      setStyle({
                        ...style,
                        title: { ...style.title, fontSize }
                      })
                    }
                  />
                </div>
              </Space>
            </div>
          </Col>
          
          <Col span={12}>
            <div style={{ marginBottom: '16px' }}>
              <h4 style={{ marginBottom: '12px', color: '#262626' }}>字幕样式</h4>
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <label style={{ display: 'block', marginBottom: 8 }}>颜色</label>
                  <ColorPicker
                    value={style.subtitle.color}
                    onChange={(color) => 
                      setStyle({
                        ...style,
                        subtitle: { ...style.subtitle, color: color.toHexString() }
                      })
                    }
                  />
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: 8 }}>位置</label>
                  <Select
                    value={style.subtitle.position}
                    onChange={(position) =>
                      setStyle({
                        ...style,
                        subtitle: { ...style.subtitle, position }
                      })
                    }
                    style={{ width: '100%' }}
                  >
                    <Select.Option value="top">顶部</Select.Option>
                    <Select.Option value="center">中间</Select.Option>
                    <Select.Option value="bottom">底部</Select.Option>
                  </Select>
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: 8 }}>
                    字体大小: {style.subtitle.fontSize}px
                  </label>
                  <Slider
                    min={10}
                    max={120}
                    value={style.subtitle.fontSize}
                    onChange={(fontSize) =>
                      setStyle({
                        ...style,
                        subtitle: { ...style.subtitle, fontSize }
                      })
                    }
                  />
                </div>
              </Space>
            </div>
          </Col>
        </Row>
      </Card>
    </Space>
  )
}

export default ConfigSettings