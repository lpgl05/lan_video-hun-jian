import React from 'react'
import { Card, Input } from '../ui'

interface BasicInfoStepProps {
  projectName: string
  onProjectNameChange: (name: string) => void
}

const BasicInfoStep: React.FC<BasicInfoStepProps> = ({
  projectName,
  onProjectNameChange
}) => {
  return (
    <div className="step-content">
      <Card 
        title="基础信息配置" 
        variant="default"
        padding="large"
        className="step-card"
      >
        <div className="form-item">
          <label className="form-label required block text-gray-900 text-sm font-medium mb-2">项目名称</label>
          <Input
            value={projectName}
            onChange={(e) => onProjectNameChange(e.target.value)}
            placeholder="请输入项目名称"
            maxLength={50}
            inputSize="large"
            variant="default"
            helperText="为您的视频混剪项目起一个有意义的名称，方便后续管理"
          />
        </div>
      </Card>
    </div>
  )
}

export default BasicInfoStep