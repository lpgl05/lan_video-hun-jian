## 项目部署

### 前端服务部署

1. 切换到前端项目目录，安装依赖

```bash
cd frontend
npm install
```

2. 运行前端项目

```bash
npm run dev
```

你会看到如下内容：  
```bash
> @video-mixer/frontend@1.0.0 dev
> vite

  VITE v5.4.19  ready in 1803 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

在浏览器中输入 `http://localhost:3000/`，即可打开前端页面。

### 后端服务部署

另外打开一个终端，首先拷贝 `env.example` 为 `.env` 文件，并根据需要填写配置信息。
```bash
# 阿里云OSS配置
OSS_ACCESS_KEY_ID=你的AccessKeyId
OSS_ACCESS_KEY_SECRET=你的AccessKeySecret
OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com
OSS_BUCKET_NAME=tian-jiu-video

# OpenAI API配置
FASTGPT_API_URL=https://api.fastgpt.in/api/v1/chat/completions
FASTGPT_API_KEY=你的API密钥
```

然后切换到后端项目目录，执行如下命令安装依赖

```bash
cd backend_py

uv venv

.venv\Scripts\activate

uv sync
```

> 注意：如果你的电脑上没有 uv 命令，请使用如下方式安装该工具。  
> 下载地址：https://github.com/astral-sh/uv/releases

由于后端服务剪辑视频使用 ffmpeg，因此需要安装 ffmpeg。下载地址如下所示：  
> https://ffmpeg.org/download.html

安装后，将 `ffmpeg` 安装目录下的 bin 目录配置到系统环境变量中。

接着运行后端服务。

```bash
uvicorn main:app --reload
```

看到如下日志，说明后端服务启动成功。  
```bash
INFO:     Will watch for changes in these directories: ['D:\\code\\tttt\\lan_video-hun-jian\\backend_py']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [13876] using StatReload
指定的字体路径是: fonts\msyh.ttc
INFO:     Started server process [15244]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

至此，前后端服务均已启动成功。可以通过访问 `http://localhost:3000/` 来使用前端服务，通过访问 `http://127.0.0.1:8000/docs` 来查看后端接口文档。