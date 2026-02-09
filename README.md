# Enhancing-Pure-Vision-BEV-3D-Perception-with-Hybrid-Data-Feature-Optimization
论文代码和数据集
1. CUDA 11.0   python3.8
2. Install mmdet3d
<pre> pip install mmcv-full==1.5.3
pip install mmdet==2.27.0
pip install mmsegmentation==0.25.0
pip install -e .  </pre>
3.Prepare nuScenes-mini dataset as introduced in nuscenes_det.md and create the pkl

4. Train and evalutate model following:
<pre> bash tools/dist_train.sh configs/sabev/clean_config.py 8 --no-validate
bash tools/dist_test.sh configs/sabev/clean_config.py work_dirs/clean_config/epoch_24_ema.pth 8 --eval bbox</pre>

Acknowledgement
This project is not possible without multiple great open-sourced code bases. We list some notable examples below.
https://github.com/mengtan00/SA-BEV/blob/master/README.md
