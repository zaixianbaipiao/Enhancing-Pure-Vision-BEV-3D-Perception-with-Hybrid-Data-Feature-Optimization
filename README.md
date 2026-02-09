# Enhancing-Pure-Vision-BEV-3D-Perception-with-Hybrid-Data-Feature-Optimization
论文代码和数据集
1. CUDA 11.0   python3.8
2. Install mmdet3d
<pre> pip install mmcv-full==1.5.3
pip install mmdet==2.27.0
pip install mmsegmentation==0.25.0
pip install -e .  </pre>

3.other requirements：
<pre>docutils==0.16.0
m2r
mistune==0.8.4
myst-parser
-e git+https://github.com/open-mmlab/pytorch_sphinx_theme.git#egg=pytorch_sphinx_theme
sphinx==4.0.2
sphinx-copybutton
sphinx_markdown_tables 
mmcv-full>=1.4.8,<=1.6.0
mmdet>=2.24.0,<=3.0.0
mmsegmentation>=0.20.0,<=1.0.0
torch
torchvision
lyft_dataset_sdk
networkx>=2.2,<2.3
numba==0.53.0
numpy
nuscenes-devkit
plyfile
scikit-image
# by default we also use tensorboard to log results
tensorboard==2.9.1
setuptools==58.0.4
trimesh>=2.35.39,<2.35.40
asynctest
codecov
flake8
interrogate
isort
# Note: used for kwarray.group_items, this may be ported to mmcv in the future.
kwarray
pytest
pytest-cov
pytest-runner
ubelt
xdoctest >= 0.10.0
yapf</pre>

  
4.Prepare nuScenes-mini dataset as introduced in nuscenes_det.md and create the pkl

5. Train and evalutate model following:
<pre> bash tools/dist_train.sh configs/sabev/clean_config.py 8 --no-validate
bash tools/dist_test.sh configs/sabev/clean_config.py work_dirs/clean_config/epoch_24_ema.pth 8 --eval bbox</pre>

Acknowledgement:

This project is not possible without multiple great open-sourced code bases. We list some notable examples below.
https://github.com/mengtan00/SA-BEV
