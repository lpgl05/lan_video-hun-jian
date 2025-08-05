### 前端服务
#### 需要往后端服务发送的请求信息
1. 文件上传相关接口

```bash
# 上传视频素材文件
POST /api/upload/video

# 上传音频（BGM）文件
POST /api/upload/audio

# 删除已上传的视频文件
DELETE /api/upload/video/:id

# 删除已上传的音频文件
DELETE /api/upload/audio/:id
```

2. AI服务相关接口

```bash
# 生成AI文案变体
# 用途：用户输入基础文案，前端调用该接口获取AI生成的多个文案变体，供用户选择。
POST /api/ai/generate-scripts
```

3. 项目管理相关接口

```bash
# 创建新项目
POST /api/projects

# 获取项目详情
GET /api/projects/:id

# 更新项目
PUT /api/projects/:id

# 删除项目
DELETE /api/projects/:id

# 获取项目列表
GET /api/projects
```

4. 视频生成相关接口

```bash
# 发起视频生成任务
POST /api/generation/start

# 查询视频生成任务状态
GET /api/generation/status/:taskId

# 取消视频生成任务
POST /api/generation/cancel/:taskId

# 获取所有生成任务列表
GET /api/generation
```

5. 健康检查与基础接口
```bash
# 检查后端服务是否可用
GET /api/ping
```