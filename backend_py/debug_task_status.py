#!/usr/bin/env python3
"""
调试任务状态和结果显示问题
"""
import asyncio
import json
from routes.clip import _task_storage

def debug_task_storage():
    """调试任务存储内容"""
    print("🔍 调试任务存储状态...")
    print(f"当前任务数量: {len(_task_storage)}")
    
    if not _task_storage:
        print("❌ 没有找到任何任务")
        return
    
    for task_id, task_data in _task_storage.items():
        print(f"\n📋 任务ID: {task_id}")
        print(f"   状态: {task_data.get('status')}")
        print(f"   进度: {task_data.get('progress')}%")
        print(f"   项目ID: {task_data.get('projectId')}")
        print(f"   创建时间: {task_data.get('createdAt')}")
        print(f"   更新时间: {task_data.get('updatedAt')}")
        
        # 重点检查result字段
        result = task_data.get('result')
        if result:
            print("   ✅ 有结果数据:")
            if isinstance(result, dict):
                videos = result.get('videos', [])
                print(f"      视频数量: {len(videos)}")
                for i, video_url in enumerate(videos):
                    print(f"      视频{i+1}: {video_url[:50]}...")
                
                preview_url = result.get('previewUrl')
                if preview_url:
                    print(f"      预览URL: {preview_url[:50]}...")
            else:
                print(f"      结果类型: {type(result)}")
                print(f"      结果内容: {result}")
        else:
            print("   ❌ 没有结果数据")
        
        # 检查错误信息
        error = task_data.get('error')
        if error:
            print(f"   ❌ 错误信息: {error}")
        
        print("-" * 50)

def create_mock_completed_task():
    """创建一个模拟的已完成任务用于测试"""
    from uuid import uuid4
    from datetime import datetime
    
    task_id = str(uuid4())
    
    mock_task = {
        "id": task_id,
        "projectId": "mock-project-id",
        "status": "completed",
        "progress": 100,
        "result": {
            "videos": [
                "https://example.com/video1.mp4",
                "https://example.com/video2.mp4",
                "https://example.com/video3.mp4"
            ],
            "previewUrl": "https://example.com/video1.mp4"
        },
        "error": None,
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    
    _task_storage[task_id] = mock_task
    
    print(f"✅ 创建了模拟任务: {task_id}")
    print(f"   状态: {mock_task['status']}")
    print(f"   视频数量: {len(mock_task['result']['videos'])}")
    
    return task_id

def test_task_api_format():
    """测试任务API返回格式"""
    print("\n🧪 测试任务API返回格式...")
    
    # 模拟API返回的数据结构
    for task_id, task_data in _task_storage.items():
        api_response = {
            "success": True,
            "data": task_data
        }
        
        print(f"\n📤 任务 {task_id} 的API响应:")
        print(json.dumps(api_response, indent=2, ensure_ascii=False))
        
        # 检查前端需要的关键字段
        data = api_response["data"]
        print(f"\n🔍 前端关键字段检查:")
        print(f"   id: {data.get('id')}")
        print(f"   status: {data.get('status')}")
        print(f"   progress: {data.get('progress')}")
        print(f"   result存在: {data.get('result') is not None}")
        
        if data.get('result'):
            result = data['result']
            print(f"   result.videos存在: {result.get('videos') is not None}")
            if result.get('videos'):
                print(f"   videos数量: {len(result['videos'])}")

def main():
    print("🚀 开始调试任务状态...")
    print("=" * 60)
    
    # 1. 检查当前任务存储
    debug_task_storage()
    
    # 2. 如果没有任务，创建一个模拟任务
    if not _task_storage:
        print("\n🎭 创建模拟任务进行测试...")
        mock_task_id = create_mock_completed_task()
        print(f"模拟任务ID: {mock_task_id}")
    
    # 3. 测试API格式
    test_task_api_format()
    
    print("\n" + "=" * 60)
    print("📋 调试总结:")
    print(f"✅ 任务总数: {len(_task_storage)}")
    
    completed_tasks = [t for t in _task_storage.values() if t.get('status') == 'completed']
    print(f"✅ 已完成任务: {len(completed_tasks)}")
    
    tasks_with_result = [t for t in _task_storage.values() if t.get('result')]
    print(f"✅ 有结果的任务: {len(tasks_with_result)}")
    
    if completed_tasks and not tasks_with_result:
        print("⚠️  问题发现: 有已完成的任务但没有结果数据！")
        print("💡 建议检查视频生成过程是否正确设置了result字段")
    elif tasks_with_result:
        print("✅ 结果数据正常，问题可能在前端显示逻辑")
    
    print("\n💡 接下来可以:")
    print("1. 检查前端GenerationResult组件的显示逻辑")
    print("2. 确认前端API调用是否正确获取任务状态")
    print("3. 查看浏览器开发者工具的网络请求和控制台日志")

if __name__ == "__main__":
    main()
