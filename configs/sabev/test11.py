# manual_test.py
import sys
import os

# 手动添加路径
custom_pipeline_path = '/home/find-aitong/SA-BEV-master/projects/sabev/pipelines'

# 确保路径在 sys.path 的最前面
if custom_pipeline_path in sys.path:
    sys.path.remove(custom_pipeline_path)
sys.path.insert(0, custom_pipeline_path)

print(f"当前 sys.path[0]: {sys.path[0]}")

# 尝试不同的导入方式
import_methods = [
    ("直接导入", "from custom_flip import SA_BEV_RandomFlip"),
    ("绝对导入", "from projects.sabev.pipelines.custom_flip import SA_BEV_RandomFlip"),
    ("相对导入", "from .custom_flip import SA_BEV_RandomFlip"),
]

for method_name, import_stmt in import_methods:
    print(f"\n尝试 {method_name}: {import_stmt}")
    try:
        exec(import_stmt)
        print(f"✓ {method_name} 成功")
        # 测试实例化
        if 'SA_BEV_RandomFlip' in locals():
            flip = SA_BEV_RandomFlip(flip_ratio=0.5, direction='horizontal')
            print(f"  ✓ 实例化成功: {flip}")
        break
    except Exception as e:
        print(f"✗ {method_name} 失败: {e}")