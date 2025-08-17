import React, { useState } from 'react'
import { message, Checkbox, Space } from 'antd'
import { EditOutlined, RobotOutlined } from '@ant-design/icons'
import type { Script } from '../types'
import { generateScripts } from '../services/api'
import { v4 as uuidv4 } from 'uuid'
import Button from './ui/Button'
import Input, { TextArea } from './ui/Input'

interface ScriptConfigProps {
  scripts: Script[]
  onScriptsChange: (scripts: Script[]) => void
  videoDuration: number
  videoCount: number
}

const ScriptConfig: React.FC<ScriptConfigProps> = ({
  scripts,
  onScriptsChange,
  videoDuration,
  videoCount,
}) => {
  const [baseScript, setBaseScript] = useState('')
  const [generating, setGenerating] = useState(false)

  const handleGenerate = async () => {
    if (!baseScript.trim()) {
      message.error('请输入基础文案')
      return
    }

    setGenerating(true)
    try {
      const result = await generateScripts(baseScript, videoDuration, videoCount)
      // 兼容后端返回字符串数组的情况
      const generatedScripts = Array.isArray(result)
        ? result.map((content: any) => ({
            id: uuidv4(),
            content: typeof content === 'string' ? content : content.content || '',
            selected: false,
            generatedAt: new Date(),
          }))
        : result
      onScriptsChange(generatedScripts)
      message.success('文案生成成功')
    } catch (error) {
      message.error('文案生成失败')
      console.error('Generate error:', error)
    } finally {
      setGenerating(false)
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
            value={baseScript}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setBaseScript(e.target.value)}
            placeholder="请输入基础文案，AI将基于此生成多个变体..."
            rows={4}
            variant="default"
            className="mb-3"
          />
          <Button
            variant="primary"
            size="middle"
            loading={generating}
            onClick={handleGenerate}
            disabled={!baseScript.trim()}
            icon={<RobotOutlined />}
          >
            AI生成文案
          </Button>
        </div>

        {scripts.length > 0 && (
          <div className="form-item">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <label className="form-label">生成的文案</label>
              <Space>
                <Button variant="outline" size="small" onClick={handleSelectAll}>
                  全选
                </Button>
                <Button variant="outline" size="small" onClick={handleDeselectAll}>
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
                      <div className="script-content">{typeof script.content === 'string' ? script.content : JSON.stringify(script.content)}</div>
                      <div className="script-meta">
                        生成时间: {script.generatedAt instanceof Date ? script.generatedAt.toLocaleString() : new Date(script.generatedAt).toLocaleString()}
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