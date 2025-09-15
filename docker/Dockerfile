FROM ubuntu:22.04

# 安装node.js ffmpeg, 直接从本地拷贝tar.gz 安装
COPY ./node-v18.0.0-linux-x64.tar.gz /tmp/
COPY ./ffmpeg-release-amd64-static.tar.xz /tmp/
COPY ./lan_video-hun-jian /opt/lan_video-hun-jian
RUN cd /tmp && \
    tar -xzf node-v18.0.0-linux-x64.tar.gz && \
    cp -r node-v18.0.0-linux-x64/* /usr/local/ && \
    rm -rf /tmp/node-v18.0.0-linux-x64* && \
    tar -xJf ffmpeg-release-amd64-static.tar.xz && \
    cp -r ffmpeg-*-amd64-static/* /usr/local/ && \
    rm -rf /tmp/ffmpeg-*-amd64-static*

# 设置环境变量
ENV NODE_HOME=/usr/local/node/bin \
    FFMPEG_HOME=/usr/local/ffmpeg/bin
