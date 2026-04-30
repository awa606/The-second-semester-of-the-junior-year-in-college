import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


from tqdm import tqdm
from data.datasets import MNIST, MNIST_1, MNIST_2
from data.loaders import create_dataloader, create_mnist_loaders

from models.base import *
from core.trainer import *
from tests.test_trainer import evaluate_on_test

def main():
   print("hello world")
   # dataset = MNIST(root_dir='./data/data/MNIST/raw')
   # dataset = MNIST_1(root_dir='./data/data/MNIST/raw')
   dataset = MNIST_2(root_dir='./data/data/MNIST/raw', image_size=28, mean_value=0.5, std_value=0.5)
   print(len(dataset))
   print(dataset[0])
   data_loader = create_dataloader(dataset)
   for batch_idx, (images, labels) in enumerate(data_loader):
       print(f"批次 {batch_idx}:")
       print(f"  图片形状: {images.shape}")  # torch.Size([16, 3, 224, 224])
       print(f"  标签形状: {labels.shape}")  # torch.Size([16])
       print(f"  数据类型: {images.dtype}")

def main_1():
    train_loader, val_loader, test_loader = create_mnist_loaders(data_dir='./data/data/MNIST/raw')
    print(len(train_loader))
    model = SimpleCNN()
    print("CNN模型结构:")
    print(model)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)

    num_epochs = 3
    trained_model, history = train_model(model, train_loader, val_loader, device, num_epochs=num_epochs, lr=0.001)
    test_acc, test_labels, test_preds, test_probs = evaluate_on_test(trained_model, test_loader, device)


if __name__ == "__main__":
    main_1()