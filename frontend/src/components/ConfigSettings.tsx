import React from 'react'
import { Card, Input, Select, Slider, Row, Col, Space, ColorPicker } from 'antd'
import type { DurationOption, VoiceOption, StyleConfig } from '../types'

interface ConfigSettingsProps {
  projectName: string
  setProjectName: (name: string) => void
  duration: DurationOption
  setDuration: (duration: DurationOption) => void
  videoCount: number
  setVideoCount: (count: number) => void
  voice: VoiceOption
  setVoice: (voice: VoiceOption) => void
  style: StyleConfig
  setStyle: (style: StyleConfig) => void
}

const ConfigSettings: React.FC<ConfigSettingsProps> = ({
  projectName,
  setProjectName,
  duration,
  setDuration,
  videoCount,
  setVideoCount,
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
              <label style={{ display: 'block', marginBottom: 8 }}>项目名称</label>
              <Input
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="请输入项目名称"
                maxLength={50}
              />
            </div>
          </Col>
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
        </Row>
        
        <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
          <Col span={12}>
            <div>
              <label style={{ display: 'block', marginBottom: 8 }}>视频数量: {videoCount}</label>
              <Slider
                min={1}
                max={10}
                value={videoCount}
                onChange={setVideoCount}
                marks={{
                  1: '1',
                  5: '5',
                  10: '10'
                }}
              />
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
            <Card title="标题样式" size="small" type="inner">
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
                    min={16}
                    max={48}
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
            </Card>
          </Col>
          
          <Col span={12}>
            <Card title="副标题样式" size="small" type="inner">
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
                    min={12}
                    max={32}
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
            </Card>
          </Col>
        </Row>
      </Card>
    </Space>
  )
}

export default ConfigSettings