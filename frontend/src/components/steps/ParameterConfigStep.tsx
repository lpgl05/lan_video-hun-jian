import React from 'react'
import ScriptConfig from '../ScriptConfig'
import ConfigSettings from '../ConfigSettings'
import { Script, VoiceOption, StyleConfig, DurationOption } from '../../types'
import { Card } from '../ui'

interface ParameterConfigStepProps {
  scripts: Script[]
  selectedScripts: string[]
  onScriptsChange: (scripts: Script[]) => void
  duration: DurationOption
  onDurationChange: (duration: DurationOption) => void
  quantity: number
  onQuantityChange: (quantity: number) => void
  voice: VoiceOption
  onVoiceChange: (voice: VoiceOption) => void
  style: StyleConfig
  onStyleChange: (style: StyleConfig) => void
}

const ParameterConfigStep: React.FC<ParameterConfigStepProps> = ({
  scripts,
  onScriptsChange,
  voice,
  onVoiceChange,
  style,
  onStyleChange,
  duration,
  onDurationChange,
  quantity,
  onQuantityChange
}) => {
  return (
    <div className="step-content">
      <Card 
        title="参数配置" 
        variant="default"
        padding="large"
      >
        <div className="flex flex-col gap-8">
          {/* 文案配置 */}
          <ScriptConfig
            scripts={scripts}
            onScriptsChange={onScriptsChange}
            videoDuration={parseInt(duration)}
            videoCount={quantity}
          />
          
          <ConfigSettings
            duration={duration}
            onDurationChange={onDurationChange}
            videoCount={quantity}
            onVideoCountChange={onQuantityChange}
            voice={voice}
            onVoiceChange={onVoiceChange}
            style={style}
            onStyleChange={onStyleChange}
          />
        </div>
      </Card>
    </div>
  )
}

export default ParameterConfigStep