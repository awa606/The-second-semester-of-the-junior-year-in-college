from tqdm import tqdm
import torch.optim as optim
from torch import nn
from core.validator import validate

import os
import torch
import json
from datetime import datetime

def train_one_epoch(model, dataloader, criterion, optimizer, device):
    """训练一个epoch"""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (data, target) in enumerate(tqdm(dataloader, desc="训练")):
        data, target = data.to(device), target.to(device)

        # 清零梯度
        optimizer.zero_grad()

        # 前向传播
        outputs = model(data)
        loss = criterion(outputs, target)

        # 反向传播
        loss.backward()
        optimizer.step()

        # 统计
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()

    epoch_loss = running_loss / len(dataloader)
    epoch_acc = 100. * correct / total

    return epoch_loss, epoch_acc


def train_model(model, train_loader, val_loader, device, num_epochs=10, lr=0.001):
    """训练模型"""
    # 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # 学习率调度器
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=2
    )

    # 记录训练历史
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': [],
        'lr': []
    }

    best_val_acc = 0.0
    best_model_state = None

    print("开始训练CNN模型...")
    print("="*60)

    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch+1}/{num_epochs}")
        print("-" * 40)

        # 训练
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)

        # 验证
        val_loss, val_acc = validate(model, val_loader, criterion, device)

        # 学习率调度
        scheduler.step(val_loss)

        # 保存最佳模型
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_model_state = model.state_dict().copy()
            print(f"保存最佳模型，验证准确率: {val_acc:.2f}%")

        # 记录历史
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        history['lr'].append(optimizer.param_groups[0]['lr'])

        # 打印进度
        print(f"训练损失: {train_loss:.4f}, 训练准确率: {train_acc:.2f}%")
        print(f"验证损失: {val_loss:.4f}, 验证准确率: {val_acc:.2f}%")
        print(f"学习率: {optimizer.param_groups[0]['lr']:.6f}")

    # 加载最佳模型
    if best_model_state is not None:
        model.load_state_dict(best_model_state)

    print("="*60)
    print(f"训练完成！最佳验证准确率: {best_val_acc:.2f}%")

    return model, history


def save_deep_learning_model(model, history, config, model_dir='models'):
    """
    保存深度学习模型
    """
    # 创建模型目录
    os.makedirs(model_dir, exist_ok=True)

    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_name = f"cnn_mnist_{timestamp}"
    model_path = os.path.join(model_dir, model_name)
    os.makedirs(model_path, exist_ok=True)

    # 保存模型参数
    model_path_pth = os.path.join(model_path, "model.pth")
    torch.save({
        'model_state_dict': model.state_dict(),
        'model_config': config,
        'training_history': history
    }, model_path_pth)

    # 保存模型结构
    model_script_path = os.path.join(model_path, "model_architecture.txt")
    with open(model_script_path, 'w') as f:
        f.write(str(model))

    # 保存模型配置
    config_path = os.path.join(model_path, "config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    # 保存训练历史
    history_path = os.path.join(model_path, "history.json")
    with open(history_path, 'w') as f:
        # 转换numpy类型为Python原生类型
        history_serializable = {}
        for key, value in history.items():
            if isinstance(value, list):
                history_serializable[key] = [float(v) for v in value]
            else:
                history_serializable[key] = float(value)
        json.dump(history_serializable, f, indent=2)

    # 保存模型为TorchScript格式（用于生产部署）
    model_scripted = torch.jit.script(model)
    model_scripted_path = os.path.join(model_path, "model_scripted.pt")
    model_scripted.save(model_scripted_path)

    print(f"深度学习模型已保存到: {model_path}")
    print(f"  模型参数: {model_path_pth}")
    print(f"  模型结构: {model_script_path}")
    print(f"  模型配置: {config_path}")
    print(f"  训练历史: {history_path}")
    print(f"  TorchScript模型: {model_scripted_path}")

    return model_path
