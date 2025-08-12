from models.oss_client import OSSClient
import asyncio

oss_client = OSSClient()


DOWNLOAD_VIDEO_PATH = "outputs/download_videos"
url = 'https://tian-jiu-video.oss-cn-beijing.aliyuncs.com/uploads/videos/eadd3ad3-1466-4133-ad4c-95c80b67a858.mp4'
filename = url.split("/")[-1]
local_file = DOWNLOAD_VIDEO_PATH + "/" + filename

async def main():
    await oss_client.download_video(url, local_file)


if __name__ == "__main__":
    asyncio.run(main())