import React, { useState, useEffect } from 'react'
import { Row, Col, Statistic, Progress, Table, DatePicker, Select } from 'antd'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, LineChart, Line, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'
import { ProjectOutlined, VideoCameraOutlined, ClockCircleOutlined, FileOutlined } from '@ant-design/icons'
import dayjs from 'dayjs'
import Card from './ui/Card'

const { RangePicker } = DatePicker
const { Option } = Select

interface UsageData {
  totalProjects: number
  totalVideos: number
  totalDuration: number
  totalStorage: number
  monthlyData: Array<{
    month: string
    projects: number
    videos: number
    duration: number
  }>
  categoryData: Array<{
    name: string
    value: number
    color: string
  }>
  recentActivity: Array<{
    date: string
    action: string
    project: string
    duration?: number
  }>
}

const UsageStatistics: React.FC = () => {
  const [timeRange, setTimeRange] = useState<'week' | 'month' | 'year'>('month')
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs | null, dayjs.Dayjs | null] | null>(null)
  const [usageData, setUsageData] = useState<UsageData>({
    totalProjects: 0,
    totalVideos: 0,
    totalDuration: 0,
    totalStorage: 0,
    monthlyData: [],
    categoryData: [],
    recentActivity: []
  })

  // 模拟数据
  useEffect(() => {
    const mockData: UsageData = {
      totalProjects: 15,
      totalVideos: 28,
      totalDuration: 3600, // 秒
      totalStorage: 2.5, // GB
      monthlyData: [
        { month: '1月', projects: 2, videos: 4, duration: 480 },
        { month: '2月', projects: 3, videos: 6, duration: 720 },
        { month: '3月', projects: 1, videos: 2, duration: 240 },
        { month: '4月', projects: 4, videos: 8, duration: 960 },
        { month: '5月', projects: 2, videos: 3, duration: 360 },
        { month: '6月', projects: 3, videos: 5, duration: 600 }
      ],
      categoryData: [
        { name: '产品宣传', value: 35, color: '#1890ff' },
        { name: '教程视频', value: 25, color: '#52c41a' },
        { name: '活动回顾', value: 20, color: '#faad14' },
        { name: '品牌故事', value: 15, color: '#f5222d' },
        { name: '其他', value: 5, color: '#722ed1' }
      ],
      recentActivity: [
        { date: '2024-12-21', action: '创建项目', project: '活动回顾', duration: 0 },
        { date: '2024-12-20', action: '完成视频', project: '产品宣传视频', duration: 120 },
        { date: '2024-12-19', action: '完成视频', project: '教程混剪', duration: 300 },
        { date: '2024-12-18', action: '创建项目', project: '品牌故事', duration: 0 },
        { date: '2024-12-17', action: '完成视频', project: '年终总结', duration: 180 }
      ]
    }
    setUsageData(mockData)
  }, [timeRange, dateRange])

  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    if (hours > 0) {
      return `${hours}小时${minutes}分钟`
    }
    return `${minutes}分钟`
  }

  const formatStorage = (gb: number) => {
    if (gb < 1) {
      return `${(gb * 1024).toFixed(0)} MB`
    }
    return `${gb.toFixed(1)} GB`
  }

  const activityColumns = [
    {
      title: '日期',
      dataIndex: 'date',
      key: 'date',
      render: (date: string) => dayjs(date).format('MM-DD')
    },
    {
      title: '操作',
      dataIndex: 'action',
      key: 'action'
    },
    {
      title: '项目',
      dataIndex: 'project',
      key: 'project'
    },
    {
      title: '时长',
      dataIndex: 'duration',
      key: 'duration',
      render: (duration: number) => duration > 0 ? formatDuration(duration) : '-'
    }
  ]

  return (
    <div className="flex flex-col gap-8">
      {/* 统计概览 */}
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={6}>
          <Card variant="default" padding="large">
            <Statistic
              title="总项目数"
              value={usageData.totalProjects}
              prefix={<ProjectOutlined style={{ color: '#4a3aff' }} />}
              valueStyle={{ 
                color: '#4a3aff',
                fontSize: '24px',
                fontWeight: '700'
              }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={6}>
          <Card variant="default" padding="large">
            <Statistic
              title="生成视频数"
              value={usageData.totalVideos}
              prefix={<VideoCameraOutlined style={{ color: '#10b981' }} />}
              valueStyle={{ 
                color: '#10b981',
                fontSize: '24px',
                fontWeight: '700'
              }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={6}>
          <Card variant="default" padding="large">
            <Statistic
              title="总时长"
              value={formatDuration(usageData.totalDuration)}
              prefix={<ClockCircleOutlined style={{ color: '#f59e0b' }} />}
              valueStyle={{ 
                color: '#f59e0b',
                fontSize: '24px',
                fontWeight: '700'
              }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={6}>
          <Card variant="default" padding="large">
            <Statistic
              title="存储使用"
              value={formatStorage(usageData.totalStorage)}
              prefix={<FileOutlined style={{ color: '#ef4444' }} />}
              valueStyle={{ 
                color: '#ef4444',
                fontSize: '24px',
                fontWeight: '700'
              }}
            />
            <Progress
              percent={(usageData.totalStorage / 10) * 100}
              size="small"
              strokeColor="var(--error-color)"
              trailColor="var(--bg-tertiary)"
              style={{ marginTop: 'var(--spacing-md)' }}
              format={() => `${((usageData.totalStorage / 10) * 100).toFixed(1)}%`}
            />
            <div style={{
              fontSize: 'var(--font-size-xs)',
              color: 'var(--text-tertiary)',
              marginTop: 'var(--spacing-xs)'
            }}>
              总容量: 10 GB
            </div>
          </Card>
        </Col>
      </Row>

      {/* 时间范围选择 */}
      <Card variant="default" padding="large" title="数据分析">
        <div style={{
          marginBottom: 'var(--spacing-lg)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div style={{ display: 'flex', gap: 'var(--spacing-md)' }}>
            <Select 
              value={timeRange} 
              onChange={setTimeRange} 
              style={{ 
                width: 120,
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-light)'
              }}
            >
              <Option value="week">最近一周</Option>
              <Option value="month">最近一月</Option>
              <Option value="year">最近一年</Option>
            </Select>
            <RangePicker
              value={dateRange}
              onChange={(dates) => setDateRange(dates)}
              placeholder={['开始日期', '结束日期']}
              style={{
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-light)'
              }}
            />
          </div>
        </div>

        <Row gutter={[16, 16]}>
          {/* 月度趋势图 */}
          <Col xs={24} lg={12}>
            <Card variant="outlined" padding="medium" title="月度项目趋势">
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={usageData.monthlyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border-light)" />
                  <XAxis dataKey="month" stroke="var(--text-secondary)" />
                  <YAxis stroke="var(--text-secondary)" />
                  <Tooltip 
                    contentStyle={{
                      background: 'var(--bg-secondary)',
                      border: '1px solid var(--border-light)',
                      borderRadius: 'var(--radius-md)',
                      boxShadow: 'var(--shadow-md)'
                    }}
                  />
                  <Legend />
                  <Line type="monotone" dataKey="projects" stroke="var(--primary-color)" name="项目数" strokeWidth={2} />
                  <Line type="monotone" dataKey="videos" stroke="var(--success-color)" name="视频数" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </Col>

          {/* 视频时长统计 */}
          <Col xs={24} lg={12}>
            <Card variant="outlined" padding="medium" title="月度视频时长">
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={usageData.monthlyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border-light)" />
                  <XAxis dataKey="month" stroke="var(--text-secondary)" />
                  <YAxis stroke="var(--text-secondary)" />
                  <Tooltip 
                    formatter={(value) => [formatDuration(value as number), '时长']}
                    contentStyle={{
                      background: 'var(--bg-secondary)',
                      border: '1px solid var(--border-light)',
                      borderRadius: 'var(--radius-md)',
                      boxShadow: 'var(--shadow-md)'
                    }}
                  />
                  <Bar dataKey="duration" fill="var(--warning-color)" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </Col>

          {/* 项目类型分布 */}
          <Col xs={24} lg={12}>
            <Card variant="outlined" padding="medium" title="项目类型分布">
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={usageData.categoryData}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                  >
                    {usageData.categoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{
                      background: 'var(--bg-secondary)',
                      border: '1px solid var(--border-light)',
                      borderRadius: 'var(--radius-md)',
                      boxShadow: 'var(--shadow-md)'
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </Card>
          </Col>

          {/* 最近活动 */}
          <Col xs={24} lg={12}>
            <Card variant="outlined" padding="medium" title="最近活动">
              <Table
                columns={activityColumns}
                dataSource={usageData.recentActivity}
                rowKey={(record, index) => `activity-${index}`}
                pagination={false}
                size="small"
                scroll={{ y: 200 }}
                style={{
                  '--table-header-bg': 'var(--bg-tertiary)',
                  '--table-header-color': 'var(--text-primary)',
                  '--table-row-hover-bg': 'var(--bg-hover)',
                  '--table-border-color': 'var(--border-light)'
                } as React.CSSProperties}
              />
            </Card>
          </Col>
        </Row>
      </Card>
    </div>
  )
}

export default UsageStatistics