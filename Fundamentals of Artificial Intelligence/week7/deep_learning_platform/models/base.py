from torch import nn
import torch.nn.functional as F
from models.layers import *

class SimpleCNN(nn.Module):
    """
    简单的卷积神经网络模型
    结构: Conv2d -> ReLU -> MaxPool2d -> Conv2d -> ReLU -> MaxPool2d -> Linear -> Dropout -> Linear
    """
    def __init__(self, dropout_rate=0.5):
        super(SimpleCNN, self).__init__()

        # 卷积层
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)  # 28x28x1 -> 28x28x32
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)  # 14x14x32 -> 14x14x64

        # 池化层
        self.pool = nn.MaxPool2d(2, 2)  # 尺寸减半

        # 全连接层
        self.fc1 = nn.Linear(64 * 7 * 7, 128)  # 7x7x64 -> 128
        self.fc2 = nn.Linear(128, 10)  # 128 -> 10 (数字0-9)

        # Dropout
        self.dropout = nn.Dropout(dropout_rate)

        # 参数初始化
        self._initialize_weights()

    def _initialize_weights(self):
        """初始化网络权重"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        # 第一层卷积
        x = self.pool(F.relu(self.conv1(x)))  # 28x28 -> 14x14
        # 第二层卷积
        x = self.pool(F.relu(self.conv2(x)))  # 14x14 -> 7x7

        # 展平
        x = x.view(-1, 64 * 7 * 7)

        # 全连接层
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        return x


class SimpleCNN_1(nn.Module):
    """
    简单的卷积神经网络模型
    结构: Conv2d -> ReLU -> MaxPool2d -> Conv2d -> ReLU -> MaxPool2d -> Linear -> Dropout -> Linear
    """
    def __init__(self, dropout_rate=0.5):
        super(SimpleCNN_1, self).__init__()

        # 卷积层
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)  # 28x28x1 -> 28x28x32
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)  # 14x14x32 -> 14x14x64

        # 池化层
        self.pool = nn.MaxPool2d(2, 2)  # 尺寸减半

        # 全连接层
        self.fc1 = nn.Linear(64 * 7 * 7, 128)  # 7x7x64 -> 128
        self.fc2 = nn.Linear(128, 10)  # 128 -> 10 (数字0-9)

        # Dropout
        self.dropout = nn.Dropout(dropout_rate)

        # activate
        self.activation = CustomActivation

        # 参数初始化
        self._initialize_weights()

    def _initialize_weights(self):
        """初始化网络权重"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        # 第一层卷积
        x = self.pool(self.activation(self.conv1(x)))  # 28x28 -> 14x14
        # 第二层卷积
        x = self.pool(self.activation(self.conv2(x)))  # 14x14 -> 7x7

        # 展平
        x = x.view(-1, 64 * 7 * 7)

        # 全连接层
        x = self.activation(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        return x


class SimpleCNN_2(nn.Module):
    """
    简单的卷积神经网络模型
    结构: Conv2d -> ReLU -> MaxPool2d -> Conv2d -> ReLU -> MaxPool2d -> Linear -> Dropout -> Linear
    """
    def __init__(self, dropout_rate=0.5):
        super(SimpleCNN_2, self).__init__()

        # 卷积模块
        self.conv_block_1 = CustomBlock(in_channels=1, out_channels=32, kernel_size=3, padding=1, kernel_size_pool=2, stride=2)
        self.conv_block_2 = CustomBlock(in_channels=32, out_channels=64, kernel_size=3, padding=1, kernel_size_pool=2,
                                        stride=2)

        # 全连接层
        self.fc1 = nn.Linear(64 * 7 * 7, 128)  # 7x7x64 -> 128
        self.fc2 = nn.Linear(128, 10)  # 128 -> 10 (数字0-9)

        # Dropout
        self.dropout = nn.Dropout(dropout_rate)

        # 参数初始化
        self._initialize_weights()

    def _initialize_weights(self):
        """初始化网络权重"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        # 第一层卷积
        x = self.conv_block_1(x)
        # 第二层卷积
        x = self.conv_block_2(x)

        # 展平
        x = x.view(-1, 64 * 7 * 7)

        # 全连接层
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        return x


class SimpleCNNWithResidual(nn.Module):
    """
    带有残差连接的卷积神经网络
    在卷积层之间添加残差连接
    """

    def __init__(self, dropout_rate=0.5):
        super(SimpleCNNWithResidual, self).__init__()

        # 第一组卷积
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)

        # 残差连接的卷积（如果维度不匹配）
        self.residual_conv = nn.Conv2d(1, 32, kernel_size=1)  # 1x1卷积调整通道数

        # 第二组卷积
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(64, 64, kernel_size=3, padding=1)

        # 池化层
        self.pool = nn.MaxPool2d(2, 2)

        # 全连接层
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

        # Dropout
        self.dropout = nn.Dropout(dropout_rate)

        # 参数初始化
        self._initialize_weights()

    def _initialize_weights(self):
        """初始化网络权重"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        # ===== 第一组卷积 + 残差连接 =====
        identity = x
        out = F.relu(self.conv1(x))
        out = F.relu(self.conv2(out))

        # 调整残差连接的维度
        identity = self.residual_conv(identity)

        # 残差连接
        out = out + identity
        out = self.pool(out)  # 14x14

        # ===== 第二组卷积 =====
        out = F.relu(self.conv3(out))
        out = F.relu(self.conv4(out))
        out = self.pool(out)  # 7x7

        # ===== 全连接层 =====
        out = out.view(out.size(0), -1)
        out = F.relu(self.fc1(out))
        out = self.dropout(out)
        out = self.fc2(out)

        return out


class SimpleCNNWithMultiScale(nn.Module):
    """
    带有多尺度特征的卷积神经网络
    在不同尺度提取特征并融合
    """

    def __init__(self, dropout_rate=0.5):
        super(SimpleCNNWithMultiScale, self).__init__()

        # 大卷积核分支（感受野大）
        self.large_kernel_conv = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=7, padding=3),  # 28x28x1 -> 28x28x16
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 14x14x16
            nn.Conv2d(16, 32, kernel_size=5, padding=2),  # 14x14x16 -> 14x14x32
            nn.ReLU(),
            nn.MaxPool2d(2, 2)  # 7x7x32
        )

        # 标准卷积核分支
        self.standard_kernel_conv = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),  # 28x28x1 -> 28x28x32
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 14x14x32
            nn.Conv2d(32, 64, kernel_size=3, padding=1),  # 14x14x32 -> 14x14x64
            nn.ReLU(),
            nn.MaxPool2d(2, 2)  # 7x7x64
        )

        # 小卷积核分支（感受野小）
        self.small_kernel_conv = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=1),  # 28x28x1 -> 28x28x64
            nn.ReLU(),
            nn.Conv2d(64, 32, kernel_size=3, padding=1),  # 28x28x64 -> 28x28x32
            nn.ReLU(),
            nn.MaxPool2d(4, 4)  # 7x7x32
        )

        # 全连接层
        # 大分支: 32 * 7 * 7 = 1568
        # 标准分支: 64 * 7 * 7 = 3136
        # 小分支: 32 * 7 * 7 = 1568
        # 总特征: 1568 + 3136 + 1568 = 6272
        self.fc1 = nn.Linear(6272, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 10)

        # Dropout
        self.dropout = nn.Dropout(dropout_rate)

        # 参数初始化
        self._initialize_weights()

    def _initialize_weights(self):
        """初始化网络权重"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        batch_size = x.size(0)

        # ===== 提取多尺度特征 =====
        features_large = self.large_kernel_conv(x)  # 7x7x32
        features_standard = self.standard_kernel_conv(x)  # 7x7x64
        features_small = self.small_kernel_conv(x)  # 7x7x32

        # 展平
        features_large = features_large.view(batch_size, -1)
        features_standard = features_standard.view(batch_size, -1)
        features_small = features_small.view(batch_size, -1)

        # ===== 特征融合 =====
        combined = torch.cat([features_large, features_standard, features_small], dim=1)

        # ===== 全连接层 =====
        out = F.relu(self.fc1(combined))
        out = self.dropout(out)
        out = F.relu(self.fc2(out))
        out = self.dropout(out)
        out = self.fc3(out)

        return out


class SimpleCNNWithAttention(nn.Module):
    """
    带有注意力分支的卷积神经网络
    注意力分支学习特征的重要性权重
    """

    def __init__(self, dropout_rate=0.5):
        super(SimpleCNNWithAttention, self).__init__()

        # 主卷积网络
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)

        # 注意力分支
        self.attention_conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.attention_conv2 = nn.Conv2d(16, 1, kernel_size=3, padding=1)
        self.attention_sigmoid = nn.Sigmoid()

        # 池化层
        self.pool = nn.MaxPool2d(2, 2)

        # 全连接层
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

        # Dropout
        self.dropout = nn.Dropout(dropout_rate)

        # 参数初始化
        self._initialize_weights()

    def _initialize_weights(self):
        """初始化网络权重"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        # ===== 生成注意力权重 =====
        attention = F.relu(self.attention_conv1(x))
        attention = self.attention_conv2(attention)
        attention_weights = self.attention_sigmoid(attention)  # 值在0-1之间

        # ===== 主分支 + 注意力加权 =====
        out = F.relu(self.conv1(x))
        out = out * attention_weights.repeat(1, 32, 1, 1)  # 应用注意力权重
        out = self.pool(out)  # 14x14

        out = F.relu(self.conv2(out))
        out = self.pool(out)  # 7x7

        # ===== 全连接层 =====
        out = out.view(out.size(0), -1)
        out = F.relu(self.fc1(out))
        out = self.dropout(out)
        out = self.fc2(out)

        return out