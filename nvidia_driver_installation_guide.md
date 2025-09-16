
# NVIDIA驱动安装指南

## 📋 安装前准备

### 1. 备份重要数据
- 创建系统还原点
- 备份重要文件

### 2. 卸载旧驱动（推荐）
- 控制面板 → 程序和功能
- 卸载所有NVIDIA相关程序：
  * NVIDIA Graphics Driver
  * NVIDIA PhysX System Software
  * NVIDIA GeForce Experience（可选保留）

### 3. 清理残留文件（可选）
- 使用DDU (Display Driver Uninstaller)
- 下载地址: https://www.guru3d.com/files-details/display-driver-uninstaller-download.html

## 🚀 安装步骤

### 方法1: 自动安装（推荐）
1. 点击下面的"自动下载并安装"按钮
2. 等待下载完成
3. 运行安装程序
4. 选择"自定义安装" → 勾选"执行清洁安装"
5. 重启电脑

### 方法2: 手动下载
1. 访问NVIDIA官网
2. 选择您的GPU型号
3. 下载最新驱动
4. 运行安装程序

### 方法3: GeForce Experience
1. 安装GeForce Experience
2. 注册/登录NVIDIA账户
3. 自动检测并安装驱动

## ✅ 安装后验证

运行以下命令验证安装：
```bash
nvidia-smi
python backend_py/simple_gpu_test.py
```

## 🔧 故障排除

### 常见问题
1. **安装失败**: 确保完全卸载旧驱动
2. **黑屏**: 重启进入安全模式，重新安装
3. **性能问题**: 检查电源设置，确保高性能模式

### 联系支持
如果遇到问题，请提供：
- nvidia-smi 输出
- 错误信息截图
- 系统配置信息
