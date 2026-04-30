import torch
from torch.utils.data import DataLoader, random_split
from data.datasets import *

def create_dataloader(dataset,
                      batch_size=32,
                      shuffle=True,
                      num_workers=4,
                      drop_last=False,
                      pin_memory=True,
                      collate_fn=None):
    """
    通用DataLoader创建函数

    Args:
        dataset: 数据集对象
        batch_size: 批次大小
        shuffle: 是否打乱数据
        num_workers: 工作进程数
        drop_last: 是否丢弃最后一个不完整的批次
        pin_memory: 是否使用固定内存
        collate_fn: 自定义批次组合函数

    Returns:
        DataLoader对象
    """
    loader = DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=pin_memory and torch.cuda.is_available(),
        drop_last=drop_last,
        collate_fn=collate_fn,
        prefetch_factor=2 if num_workers > 0 else None,
        persistent_workers=num_workers > 0
    )

    return loader


def create_mnist_loaders(data_dir='./data/mnist/raw',
                         batch_size=64,
                         val_ratio=0.1,
                         num_workers=4,
                         n_train=10000,
                         download=True):
    """
    创建MNIST数据集的DataLoader

    Args:
        data_dir: 数据目录
        batch_size: 批次大小
        val_ratio: 验证集比例
        num_workers: 数据加载工作进程数
        download: 是否自动下载数据

    Returns:
        train_loader, val_loader, test_loader
    """
    # 获取数据变换
    # train_transform = get_transforms('mnist', is_train=True)
    # test_transform = get_transforms('mnist', is_train=False)

    # 创建完整训练集
    train_dataset = MNIST_3(
        root_dir=data_dir,
        is_train=True,
    )

    # 创建测试集
    test_dataset = MNIST_3(
        root_dir=data_dir,
        is_train=False,
    )

    # 分割训练集为训练和验证
    train_size = len(train_dataset)
    val_size = int(train_size * val_ratio)
    train_size = train_size - val_size

    train_dataset, val_dataset = random_split(
        train_dataset,
        [train_size, val_size],
        generator=torch.Generator().manual_seed(42)  # 固定随机种子
    )

    # 创建DataLoader
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )

    return train_loader, val_loader, test_loader