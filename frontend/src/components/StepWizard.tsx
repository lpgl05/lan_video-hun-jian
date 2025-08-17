import React from 'react'
import { Steps } from 'antd'
import { CheckCircleOutlined, LoadingOutlined } from '@ant-design/icons'

interface StepWizardProps {
  currentStep: number
  onStepChange: (step: number) => void
  steps: {
    title: string
    description?: string
    disabled?: boolean
  }[]
  className?: string
}

const StepWizard: React.FC<StepWizardProps> = ({
  currentStep,
  onStepChange,
  steps,
  className = ''
}) => {
  const handleStepClick = (step: number) => {
    if (!steps[step]?.disabled) {
      onStepChange(step)
    }
  }

  return (
    <div className={`step-wizard ${className}`}>
      <Steps
        current={currentStep}
        onChange={handleStepClick}
        type="navigation"
        size="small"
        className="step-navigation"
      >
        {steps.map((step, index) => (
          <Steps.Step
            key={index}
            title={step.title}
            description={step.description}
            disabled={step.disabled}
            icon={
              index < currentStep ? (
                <CheckCircleOutlined className="text-green-500" />
              ) : index === currentStep ? (
                <LoadingOutlined className="text-blue-500" />
              ) : undefined
            }
          />
        ))}
      </Steps>
    </div>
  )
}

export default StepWizard