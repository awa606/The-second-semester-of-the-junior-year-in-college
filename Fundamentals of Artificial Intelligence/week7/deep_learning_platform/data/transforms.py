import torchvision.transforms as T
from torchvision.transforms import functional as F
import random
import torch
from PIL import Image

class BasicTransforms:
    """基本变换工厂类"""

    @staticmethod
    def get_transform(img_size, mean, std):
        """获取基本变换"""
        return T.Compose([
            T.Resize((img_size, img_size)),
            T.ToTensor(),
            T.Normalize(mean=mean, std=std)
        ])