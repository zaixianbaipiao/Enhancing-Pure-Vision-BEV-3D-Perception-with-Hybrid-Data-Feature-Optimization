import numpy as np
import mmcv
import torch
from mmdet.datasets import PIPELINES
from mmdet3d.core.bbox import LiDARInstance3DBoxes

@PIPELINES.register_module()
class SA_BEV_RandomFlip:
    """专为 SA-BEV 模型设计的随机翻转模块"""
    
    def __init__(self, flip_ratio=0.2, direction='horizontal'):
        self.flip_ratio = flip_ratio
        if direction not in ['horizontal', 'vertical']:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")
        self.direction = direction
        # 添加初始化日志（唯一标识：[SA_BEV_Init]）
        #print(f"[SA_BEV_Init] Module initialized: flip_ratio={self.flip_ratio}, direction={self.direction}")
        
    def flip_image(self, img):
        if isinstance(img, np.ndarray):
            return mmcv.imflip(img, direction=self.direction)
        elif isinstance(img, torch.Tensor):
            if self.direction == 'horizontal':
                return img.flip(-1)
            else:
                return img.flip(-2)
        return img
    
    def flip_bboxes_3d(self, bboxes, img_shape):
        if bboxes is None:
            return bboxes
            
        boxes_np = bboxes.tensor.numpy().copy()
        
        if self.direction == 'horizontal':
            boxes_np[:, 1] = -boxes_np[:, 1]
            boxes_np[:, 6] = -boxes_np[:, 6]
        else:
            boxes_np[:, 2] = -boxes_np[:, 2]
            boxes_np[:, 6] = np.pi - boxes_np[:, 6]
            
        flipped_bboxes = LiDARInstance3DBoxes(
            torch.from_numpy(boxes_np), box_dim=bboxes.tensor.size(1)
        )
        return flipped_bboxes
    
    def flip_depth_map(self, depth_map):
        if depth_map is None:
            return depth_map
            
        if isinstance(depth_map, np.ndarray):
            if self.direction == 'horizontal':
                return np.fliplr(depth_map)
            else:
                return np.flipud(depth_map)
        elif isinstance(depth_map, torch.Tensor):
            if self.direction == 'horizontal':
                return depth_map.flip(-1)
            else:
                return depth_map.flip(-2)
        return depth_map
    
    def flip_semantic_map(self, semantic_map):
        if semantic_map is None:
            return semantic_map
            
        if isinstance(semantic_map, np.ndarray):
            if self.direction == 'horizontal':
                return np.fliplr(semantic_map)
            else:
                return np.flipud(semantic_map)
        elif isinstance(semantic_map, torch.Tensor):
            if self.direction == 'horizontal':
                return semantic_map.flip(-1)
            else:
                return semantic_map.flip(-2)
        return semantic_map
    
    def __call__(self, results):
         # 节点1：模块被调用（每个样本都会触发）
        #print(f"[SA_BEV_Call] Start processing sample, flip_ratio={self.flip_ratio}")
        if np.random.rand() > self.flip_ratio:
            return results
        # 节点2：生成随机数，判断是否翻转
        rand_val = np.random.rand()
        do_flip = rand_val <= self.flip_ratio
        #print(f"[SA_BEV_FlipCheck] Random value: {rand_val:.4f}, Flip? {do_flip} (ratio={self.flip_ratio})")
    
        if not do_flip:
            # 节点3：未触发翻转，直接返回
            #print(f"[SA_BEV_Skip] Skip flip (rand > flip_ratio), return original data")
            return results    
        # 翻转图像数据
        if 'img_inputs' in results:
            img_data = results['img_inputs']
            
            if isinstance(img_data, list):
                flipped_imgs = []
                for img in img_data:
                    flipped_imgs.append(self.flip_image(img))
                results['img_inputs'] = flipped_imgs
                
            elif isinstance(img_data, np.ndarray):
                if img_data.ndim == 4:
                    if self.direction == 'horizontal':
                        results['img_inputs'] = img_data[:, :, :, ::-1].copy()
                    else:
                        results['img_inputs'] = img_data[:, :, ::-1, :].copy()
                elif img_data.ndim == 3:
                    if self.direction == 'horizontal':
                        results['img_inputs'] = img_data[:, :, ::-1].copy()
                    else:
                        results['img_inputs'] = img_data[:, ::-1, :].copy()
                        
            elif isinstance(img_data, tuple):
                flipped_imgs = []
                for img in img_data:
                    flipped_imgs.append(self.flip_image(img))
                results['img_inputs'] = tuple(flipped_imgs)
        
        # 翻转3D边界框
        if 'gt_bboxes_3d' in results and results['gt_bboxes_3d'] is not None:
            img_shape = results.get('img_shape', (900, 1600))
            results['gt_bboxes_3d'] = self.flip_bboxes_3d(
                results['gt_bboxes_3d'], img_shape
            )
        
        # 翻转深度图
        if 'gt_depth' in results and results['gt_depth'] is not None:
            results['gt_depth'] = self.flip_depth_map(results['gt_depth'])
        
        # 翻转语义分割图
        if 'gt_semantic' in results and results['gt_semantic'] is not None:
            results['gt_semantic'] = self.flip_semantic_map(results['gt_semantic'])
        
        results['flipped'] = True
        results['flip_direction'] = self.direction
        #print(f"[SA_BEV_Done] Flip completed! Marked results['flipped']=True, direction={self.direction}")# 节点:标记翻转结果
        return results
    
    def __repr__(self):
        return f"{self.__class__.__name__}(flip_ratio={self.flip_ratio}, direction='{self.direction}')"