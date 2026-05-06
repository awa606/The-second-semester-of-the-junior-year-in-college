import argparse
import os
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from tqdm import tqdm


class CIFAR10CNN(nn.Module):
    """用于 CIFAR-10 图像分类的卷积神经网络。"""

    def __init__(self) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Dropout(0.25),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Dropout(0.25),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Dropout(0.25),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, 10),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.classifier(x)
        return x


def set_seed(seed: int = 42) -> None:
    """设置随机种子，保证结果尽可能可复现。"""
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)


def build_dataloaders(data_dir: str, batch_size: int, num_workers: int) -> Tuple[DataLoader, DataLoader, DataLoader, List[str]]:
    """构建训练、验证、测试数据加载器。"""
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])

    transform_eval = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])

    full_train_dataset = datasets.CIFAR10(root=data_dir, train=True, download=True)
    class_names = full_train_dataset.classes

    train_size = int(0.9 * len(full_train_dataset))
    val_size = len(full_train_dataset) - train_size

    train_subset, val_subset = random_split(
        full_train_dataset,
        [train_size, val_size],
        generator=torch.Generator().manual_seed(42),
    )

    # 为切分后的训练/验证集分别指定不同变换
    train_subset.dataset = datasets.CIFAR10(root=data_dir, train=True, download=True, transform=transform_train)
    val_subset.dataset = datasets.CIFAR10(root=data_dir, train=True, download=True, transform=transform_eval)

    test_dataset = datasets.CIFAR10(root=data_dir, train=False, download=True, transform=transform_eval)

    train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True)

    return train_loader, val_loader, test_loader, class_names


def run_one_epoch(model: nn.Module, data_loader: DataLoader, criterion: nn.Module, device: torch.device, optimizer=None) -> Tuple[float, float]:
    """运行一个训练/验证轮次并返回损失与准确率。"""
    is_train = optimizer is not None
    model.train() if is_train else model.eval()

    running_loss = 0.0
    correct = 0
    total = 0

    with torch.set_grad_enabled(is_train):
        for images, labels in tqdm(data_loader, leave=False):
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            if is_train:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            running_loss += loss.item() * labels.size(0)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc


def test_model(model: nn.Module, data_loader: DataLoader, criterion: nn.Module, device: torch.device) -> Tuple[float, float, np.ndarray, np.ndarray]:
    """在测试集上评估模型并返回指标与预测结果。"""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    all_labels = []
    all_preds = []

    with torch.no_grad():
        for images, labels in tqdm(data_loader, desc="Testing", leave=False):
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * labels.size(0)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

            all_labels.extend(labels.cpu().numpy())
            all_preds.extend(preds.cpu().numpy())

    return running_loss / total, correct / total, np.array(all_labels), np.array(all_preds)


def plot_training_curve(history: Dict[str, List[float]], save_path: str) -> None:
    """绘制并保存训练过程曲线。"""
    epochs = range(1, len(history["train_loss"]) + 1)
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(epochs, history["train_loss"], label="Train Loss")
    plt.plot(epochs, history["val_loss"], label="Val Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training / Validation Loss")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs, history["train_acc"], label="Train Acc")
    plt.plot(epochs, history["val_acc"], label="Val Acc")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Training / Validation Accuracy")
    plt.legend()

    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()


def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, class_names: List[str], save_path: str) -> None:
    """绘制并保存测试集混淆矩阵。"""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(8, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
    disp.plot(cmap="Blues", ax=ax, xticks_rotation=45, colorbar=False)
    plt.title("CIFAR-10 Test Confusion Matrix")
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="CIFAR-10 CNN 训练与测试脚本")
    parser.add_argument("--epochs", type=int, default=20, help="训练轮数，默认 20")
    parser.add_argument("--batch_size", type=int, default=128, help="批大小，默认 128")
    parser.add_argument("--lr", type=float, default=1e-3, help="学习率，默认 1e-3")
    parser.add_argument("--data_dir", type=str, default="./data", help="数据集下载目录")
    parser.add_argument("--num_workers", type=int, default=2, help="DataLoader 线程数，默认 2")
    args = parser.parse_args()

    set_seed(42)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    data_dir = os.path.join(base_dir, args.data_dir)
    train_loader, val_loader, test_loader, class_names = build_dataloaders(
        data_dir=data_dir,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
    )

    model = CIFAR10CNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)

    best_val_acc = 0.0
    best_model_path = os.path.join(output_dir, "best_cifar10_cnn.pth")
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    for epoch in range(1, args.epochs + 1):
        train_loss, train_acc = run_one_epoch(model, train_loader, criterion, device, optimizer=optimizer)
        val_loss, val_acc = run_one_epoch(model, val_loader, criterion, device, optimizer=None)
        scheduler.step()

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)

        print(
            f"Epoch [{epoch:02d}/{args.epochs:02d}] "
            f"Train Loss: {train_loss:.4f} Train Acc: {train_acc:.4f} "
            f"Val Loss: {val_loss:.4f} Val Acc: {val_acc:.4f}"
        )

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), best_model_path)
            print(f"  -> Best model updated and saved to: {best_model_path}")

    training_curve_path = os.path.join(output_dir, "training_curve.png")
    plot_training_curve(history, training_curve_path)
    print(f"Training curve saved to: {training_curve_path}")

    model.load_state_dict(torch.load(best_model_path, map_location=device))
    test_loss, test_acc, y_true, y_pred = test_model(model, test_loader, criterion, device)

    cm_path = os.path.join(output_dir, "test_confusion_matrix.png")
    plot_confusion_matrix(y_true, y_pred, class_names, cm_path)

    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_acc * 100:.2f}%")
    print(f"Test confusion matrix saved to: {cm_path}")


if __name__ == "__main__":
    main()
