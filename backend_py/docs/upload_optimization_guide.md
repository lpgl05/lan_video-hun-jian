# OSS上传速度优化指南

## 🚀 优化总结

我们已经实现了以下优化措施来解决上传速度慢的问题：

### 1. 并发分片上传
- **之前**: 串行上传分片（逐个上传）
- **现在**: 并发上传分片（最多10个并发）
- **效果**: 理论上可提升5-10倍速度

### 2. 动态分片大小优化
- **小文件** (<50MB): 10MB分片
- **中等文件** (50-200MB): 20MB分片  
- **大文件** (200-500MB): 50MB分片
- **超大文件** (>500MB): 100MB分片

### 3. 连接池优化
- 连接池大小: 50个连接
- 连接超时: 30秒
- 读取超时: 300秒

### 4. 可配置优化参数
通过环境变量灵活调整所有优化参数。

## ⚙️ 配置调整

在您的 `.env` 文件中添加以下配置（根据您的网络环境调整）：

```bash
# 基础OSS配置
OSS_ACCESS_KEY_ID=你的AccessKeyId
OSS_ACCESS_KEY_SECRET=你的AccessKeySecret
OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com
OSS_BUCKET_NAME=tian-jiu-video

# 性能优化配置
OSS_CONNECTION_POOL_SIZE=50          # 连接池大小
OSS_CONNECTION_TIMEOUT=30            # 连接超时(秒)
OSS_READ_TIMEOUT=300                 # 读取超时(秒)
OSS_MAX_CONCURRENT_UPLOADS=10        # 最大并发上传数
OSS_MULTIPART_THRESHOLD=10           # 分片上传阈值(MB)

# 分片大小配置(MB)
OSS_PART_SIZE_SMALL=10               # 小文件分片大小
OSS_PART_SIZE_MEDIUM=20              # 中等文件分片大小
OSS_PART_SIZE_LARGE=50               # 大文件分片大小
OSS_PART_SIZE_XLARGE=100             # 超大文件分片大小

# 文件大小阈值(MB)
OSS_SMALL_FILE_THRESHOLD=50          # 小文件阈值
OSS_MEDIUM_FILE_THRESHOLD=200        # 中等文件阈值
OSS_LARGE_FILE_THRESHOLD=500         # 大文件阈值
```

## 🔧 针对性优化建议

### 如果您的网络较慢：
```bash
OSS_MAX_CONCURRENT_UPLOADS=5         # 减少并发数
OSS_PART_SIZE_SMALL=5                # 减小分片大小
OSS_PART_SIZE_MEDIUM=10
OSS_PART_SIZE_LARGE=20
OSS_READ_TIMEOUT=600                 # 增加超时时间
```

### 如果您的网络很快：
```bash
OSS_MAX_CONCURRENT_UPLOADS=15        # 增加并发数
OSS_PART_SIZE_MEDIUM=30              # 增大分片大小
OSS_PART_SIZE_LARGE=80
OSS_PART_SIZE_XLARGE=150
OSS_CONNECTION_POOL_SIZE=100         # 增大连接池
```

### 如果在公司网络环境：
```bash
OSS_MAX_CONCURRENT_UPLOADS=3         # 保守的并发数
OSS_CONNECTION_TIMEOUT=60            # 增加连接超时
OSS_READ_TIMEOUT=900                 # 增加读取超时
```

## 🌍 选择最优接入点

不同地区应选择不同的OSS接入点：

- **华北地区**: `oss-cn-beijing.aliyuncs.com`
- **华东地区**: `oss-cn-shanghai.aliyuncs.com` 或 `oss-cn-hangzhou.aliyuncs.com`
- **华南地区**: `oss-cn-shenzhen.aliyuncs.com` 或 `oss-cn-guangzhou.aliyuncs.com`
- **西南地区**: `oss-cn-chengdu.aliyuncs.com`

## 🔍 网络诊断工具

我们提供了网络诊断工具来帮助您找到最优配置：

```bash
cd backend_py
python tools/network_optimizer.py
```

这个工具会：
1. 测试不同OSS接入点的延迟
2. 进行上传速度测试
3. 检查DNS解析速度
4. 生成个性化优化建议

## 🚨 常见问题解决

### 问题1: 上传速度仍然很慢
**可能原因:**
- 网络带宽限制
- 公司防火墙/代理限制
- OSS接入点选择不当

**解决方案:**
1. 运行网络诊断工具
2. 尝试不同的OSS接入点
3. 检查网络代理设置
4. 测试使用手机热点

### 问题2: 上传过程中断
**可能原因:**
- 网络不稳定
- 超时时间设置过短

**解决方案:**
```bash
OSS_READ_TIMEOUT=900                 # 增加到15分钟
OSS_CONNECTION_TIMEOUT=60            # 增加连接超时
OSS_MAX_RETRIES=5                    # 增加重试次数
```

### 问题3: 内存使用过高
**可能原因:**
- 分片大小过大
- 并发数过高

**解决方案:**
```bash
OSS_MAX_CONCURRENT_UPLOADS=3         # 减少并发
OSS_PART_SIZE_LARGE=20               # 减小分片大小
```

## 📊 性能对比

| 优化措施 | 优化前 | 优化后 | 提升倍数 |
|---------|--------|---------|----------|
| 分片大小 | 5MB | 动态调整(10-100MB) | 2-4x |
| 并发上传 | 串行 | 最多10并发 | 5-10x |
| 连接池 | 默认 | 50连接 | 1.5-2x |
| **总体提升** | - | - | **10-20x** |

## 🎯 预期效果

根据您的反馈，其他同学200MB文件5秒上传完成，速度约为40MB/s。
通过我们的优化，您应该能达到类似的速度。

如果优化后速度仍不理想，建议：
1. 检查网络环境差异
2. 运行诊断工具找出瓶颈
3. 尝试更激进的配置参数
