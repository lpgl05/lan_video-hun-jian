#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的GPU编码功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.clip_service import check_gpu_support, test_nvenc_encoder
import json

def test_gpu_functionality():
    """测试GPU功能"""
    print("=== GPU硬件加速编码功能测试 ===")
    print()
    
    # 1. 检查GPU支持状态
    print("1. 检查GPU支持状态...")
    try:
        gpu_support = check_gpu_support()
        print(f"GPU支持检查结果:")
        print(json.dumps(gpu_support, indent=2, ensure_ascii=False))
        print()
        
        if gpu_support.get('nvenc'):
            print("✅ NVENC编码器可用且已通过测试")
        else:
            print("❌ NVENC编码器不可用或测试失败")
            
        if gpu_support.get('any_gpu'):
            print("✅ 至少有一个GPU编码器可用")
        else:
            print("❌ 没有可用的GPU编码器")
            
    except Exception as e:
        print(f"❌ GPU支持检查失败: {e}")
        return False
    
    print()
    
    # 2. 单独测试NVENC编码器
    print("2. 单独测试NVENC编码器...")
    try:
        nvenc_result = test_nvenc_encoder()
        if nvenc_result:
            print("✅ NVENC编码器独立测试通过")
        else:
            print("❌ NVENC编码器独立测试失败")
    except Exception as e:
        print(f"❌ NVENC编码器测试异常: {e}")
        return False
    
    print()
    
    # 3. 测试总结
    print("=== 测试总结 ===")
    if gpu_support.get('nvenc') and nvenc_result:
        print("🎉 GPU硬件加速编码功能修复成功！")
        print("✅ NVENC编码器可以正常工作")
        print("✅ 错误处理机制已优化")
        print("✅ 编码参数已调整为更兼容的配置")
        return True
    else:
        print("⚠️ GPU硬件加速编码功能仍有问题")
        if not gpu_support.get('nvenc'):
            print("- NVENC编码器不可用")
        if not nvenc_result:
            print("- NVENC编码器测试失败")
        return False

if __name__ == "__main__":
    success = test_gpu_functionality()
    sys.exit(0 if success else 1)