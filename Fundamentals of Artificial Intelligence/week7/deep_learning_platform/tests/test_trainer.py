import numpy as np
import torch
from tqdm import tqdm
import torch.nn.functional as F

def evaluate_on_test(model, test_loader, device):
    """在测试集上评估模型"""
    model.eval()
    all_labels = []
    all_predictions = []
    all_probs = []

    correct = 0
    total = 0

    with torch.no_grad():
        for data, target in tqdm(test_loader, desc="测试"):
            data, target = data.to(device), target.to(device)
            outputs = model(data)

            # 获取预测结果
            probs = F.softmax(outputs, dim=1)
            _, predicted = outputs.max(1)

            # 统计
            total += target.size(0)
            correct += predicted.eq(target).sum().item()

            # 保存结果用于分析
            all_labels.extend(target.cpu().numpy())
            all_predictions.extend(predicted.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())

    test_accuracy = 100. * correct / total

    print("="*60)
    print(f"测试集准确率: {test_accuracy:.2f}%")
    print(f"正确数: {correct}/{total}")
    print("="*60)

    return test_accuracy, np.array(all_labels), np.array(all_predictions), np.array(all_probs)