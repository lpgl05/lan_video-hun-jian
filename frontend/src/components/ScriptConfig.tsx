import React, { useState } from 'react'
import { Input, Button, message, Checkbox, Space, Progress } from 'antd'
import { EditOutlined, RobotOutlined } from '@ant-design/icons'
import type { Script } from '../types'
import { generateScripts } from '../services/api'
import { v4 as uuidv4 } from 'uuid'

const { TextArea } = Input

interface ScriptConfigProps {
  scripts: Script[]
  onScriptsChange: (scripts: Script[]) => void
  videoDuration: number
  videoCount: number
  baseScript?: string
  onBaseScriptChange?: (script: string) => void
}

const ScriptConfig: React.FC<ScriptConfigProps> = ({
  scripts,
  onScriptsChange,
  videoDuration,
  videoCount,
  baseScript = '',
  onBaseScriptChange,
}) => {
  const [localBaseScript, setLocalBaseScript] = useState(baseScript)
  const [generating, setGenerating] = useState(false)
  const [generateProgress, setGenerateProgress] = useState(0)

  const handleBaseScriptChange = (value: string) => {
    setLocalBaseScript(value)
    onBaseScriptChange?.(value)
  }

  const handleGenerate = async () => {
    if (!localBaseScript.trim()) {
      message.error('请输入基础文案')
      return
    }

    setGenerating(true)
    setGenerateProgress(50) // 从50%开始
    
    // 模拟进度条
    const progressInterval = setInterval(() => {
      setGenerateProgress(prev => {
        if (prev >= 85) {
          return Math.min(prev + 0.5, 95) // 85%后缓慢增长，最大到95%
        }
        const increment = Math.random() * 8 + 2 // 2-10%的随机增长
        return Math.min(prev + increment, 85) // 确保不超过85%
      })
    }, 300)

    try {
      const result = await generateScripts(localBaseScript, videoDuration, videoCount)
      
      // 清除进度模拟，设置为100%
      clearInterval(progressInterval)
      setGenerateProgress(100)
      
      // 兼容后端返回字符串数组的情况
      const generatedScripts = Array.isArray(result)
        ? result.map((content: string) => ({
            id: uuidv4(),
            content,
            selected: true, // 默认选中所有生成的文案
            generatedAt: new Date(),
          }))
        : result.map((script: any) => ({
            ...script,
            selected: true // 如果是对象数组，也默认选中
          }))
      onScriptsChange(generatedScripts)
      message.success('文案生成成功')
    } catch (error) {
      clearInterval(progressInterval)
      setGenerateProgress(0)
      message.error('文案生成失败')
      console.error('Generate error:', error)
    } finally {
      setGenerating(false)
      
      // 稍微延迟重置进度条，让用户看到100%
      setTimeout(() => {
        setGenerateProgress(0)
      }, 1000)
    }
  }

  const handleScriptToggle = (scriptId: string) => {
    const updatedScripts = scripts.map(script => 
      script.id === scriptId 
        ? { ...script, selected: !script.selected }
        : script
    )
    onScriptsChange(updatedScripts)
  }

  const handleSelectAll = () => {
    const updatedScripts = scripts.map(script => ({ ...script, selected: true }))
    onScriptsChange(updatedScripts)
  }

  const handleDeselectAll = () => {
    const updatedScripts = scripts.map(script => ({ ...script, selected: false }))
    onScriptsChange(updatedScripts)
  }

  const selectedCount = scripts.filter(s => s.selected).length

  return (
    <div className="section">
      <div className="section-title">
        <EditOutlined />
        文案配置 ({selectedCount}/{scripts.length} 已选择)
      </div>
      
      <div className="section-content">
        <div className="form-item">
          <label className="form-label">基础文案</label>
          <TextArea
            value={localBaseScript}
            onChange={(e) => handleBaseScriptChange(e.target.value)}
            placeholder="请输入基础文案，AI将基于此生成多个变体..."
            rows={4}
            style={{ marginBottom: '12px' }}
          />
          <Button
            type="primary"
            icon={<RobotOutlined />}
            loading={generating}
            onClick={handleGenerate}
            disabled={!localBaseScript.trim()}
          >
            AI生成文案
          </Button>
          
          {/* AI生成进度条 */}
          {generating && generateProgress > 0 && (
            <div style={{ marginTop: '16px' }}>
              <div style={{ 
                marginBottom: '8px', 
                fontSize: '14px', 
                color: '#666',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <span>AI正在生成文案...</span>
                <span>{Math.min(Math.round(generateProgress), 100)}%</span>
              </div>
              <Progress
                percent={Math.min(Math.round(generateProgress), 100)}
                status={generateProgress >= 100 ? 'success' : 'active'}
                strokeColor={{
                  '0%': '#1890ff',
                  '50%': '#722ed1',
                  '100%': '#52c41a'
                }}
                size={6}
                showInfo={false}
              />
            </div>
          )}
        </div>

        {scripts.length > 0 && (
          <div className="form-item">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <label className="form-label">生成的文案</label>
              <Space>
                <Button size="small" onClick={handleSelectAll}>
                  全选
                </Button>
                <Button size="small" onClick={handleDeselectAll}>
                  取消全选
                </Button>
              </Space>
            </div>
            
            <div className="script-list">
              {scripts.map((script) => (
                <div 
                  key={script.id} 
                  className={`script-item ${script.selected ? 'selected' : ''}`}
                  onClick={() => handleScriptToggle(script.id)}
                >
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                    <Checkbox 
                      checked={script.selected}
                      onChange={() => handleScriptToggle(script.id)}
                      onClick={(e) => e.stopPropagation()}
                    />
                    <div style={{ flex: 1 }}>
                      <div className="script-content">{script.content}</div>
                      <div className="script-meta">
                        生成时间: {new Date(script.generatedAt).toLocaleString()}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ScriptConfig