import torch
from torch import nn
import torch.nn.functional as F


class CustomActivation(nn.Module):
    """
    自定义激活函数层
    演示如何创建新的激活函数
    """

    def __init__(self, alpha=0.1):
        """
        初始化

        Args:
            alpha: 负值区域的斜率
        """
        super().__init__()
        self.alpha = nn.Parameter(torch.tensor(alpha, dtype=torch.float32))

    def forward(self, x):
        """
        前向传播

        Args:
            x: 输入张量

        Returns:
            y: 应用激活函数后的张量
        """
        # 实现一个简单的自定义激活函数
        # 类似于LeakyReLU，但参数可学习
        return torch.where(x > 0, x, self.alpha * x)

    def extra_repr(self):
        return f'alpha={self.alpha.item():.3f}'


class SwishActivation(nn.Module):
    """
    Swish激活函数: x * sigmoid(beta * x)
    这是一个流行的自定义激活函数
    """

    def __init__(self, beta=1.0, trainable=False):
        """
        初始化

        Args:
            beta: Swish函数的参数
            trainable: beta是否可训练
        """
        super().__init__()

        if trainable:
            self.beta = nn.Parameter(torch.tensor(beta, dtype=torch.float32))
        else:
            self.beta = beta

        self.trainable = trainable

    def forward(self, x):
        """前向传播"""
        beta = self.beta if not self.trainable else torch.sigmoid(self.beta) * 2
        return x * torch.sigmoid(beta * x)

    def extra_repr(self):
        beta_val = self.beta.item() if hasattr(self.beta, 'item') else self.beta
        return f'beta={beta_val:.3f}, trainable={self.trainable}'


class CustomBlock(nn.Module):
    """
    自定义块：组合多个自定义层
    展示如何构建复杂的自定义模块
    """

    def __init__(self, in_channels, out_channels, kernel_size=3,  padding=1, kernel_size_pool=2, stride=2):
        super(CustomBlock, self).__init__()
        # 卷积层
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        # 池化层
        self.pool = nn.MaxPool2d(kernel_size_pool, stride)  # 尺寸减半

    def forward(self, x):
        out = self.pool(F.relu(self.conv1(x)))
        return out

