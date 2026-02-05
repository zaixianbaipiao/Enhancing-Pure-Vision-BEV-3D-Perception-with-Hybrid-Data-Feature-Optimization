# debug_paths.py
import sys
import os

print("=== Python 路径诊断 ===")
print(f"Python 可执行文件: {sys.executable}")
print(f"Python 版本: {sys.version}")

print("\n=== sys.path 内容 ===")
for i, path in enumerate(sys.path):
    print(f"{i}: {path}")

print("\n=== 检查自定义模块路径 ===")
project_root = '/home/find-aitong/SA-BEV-master'
custom_pipeline_path = '/home/find-aitong/SA-BEV-master/projects/sabev/pipelines'

print(f"项目根目录: {project_root}")
print(f"自定义管道路径: {custom_pipeline_path}")

print(f"\n项目根目录是否存在: {os.path.exists(project_root)}")
print(f"自定义管道路径是否存在: {os.path.exists(custom_pipeline_path)}")

print(f"\n项目根目录是否在 sys.path: {project_root in sys.path}")
print(f"自定义管道路径是否在 sys.path: {custom_pipeline_path in sys.path}")

# 检查 __init__.py 文件
init_file = os.path.join(custom_pipeline_path, '__init__.py')
print(f"\n__init__.py 文件是否存在: {os.path.exists(init_file)}")

# 列出自定义管道路径中的所有 Python 文件
if os.path.exists(custom_pipeline_path):
    print(f"\n自定义管道路径中的文件:")
    for file in os.listdir(custom_pipeline_path):
        print(f"  - {file}")