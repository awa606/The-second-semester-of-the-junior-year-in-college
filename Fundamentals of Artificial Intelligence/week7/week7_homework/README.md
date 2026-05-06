# 深度学习项目开发实践：CIFAR-10 卷积神经网络分类

## 一、项目目标
本作业基于 PyTorch 与 torchvision 完成 CIFAR-10 十分类任务，包含：
- 数据自动下载与加载
- 数据增强与归一化
- CNN 模型训练、验证、测试
- 训练指标（Loss / Accuracy）记录
- 最佳模型保存
- 训练曲线图与测试混淆矩阵图自动保存

## 二、目录结构
```text
week7_homework/
├── README.md
├── requirements.txt
├── cifar10_cnn_train_test.py
├── outputs/
│   └── .gitkeep
└── screenshots/
    └── .gitkeep
```

> 说明：运行脚本后会在 `outputs/` 下生成模型与图片结果文件。

## 三、环境安装
建议在虚拟环境中执行：

```bash
pip install -r requirements.txt
```

## 四、训练与测试命令
进入当前目录后执行：

```bash
python cifar10_cnn_train_test.py
```

默认训练 20 轮，可通过参数修改，例如训练 5 轮：

```bash
python cifar10_cnn_train_test.py --epochs 5
```

常用可选参数：
- `--batch_size`：批大小（默认 128）
- `--lr`：学习率（默认 1e-3）
- `--num_workers`：数据加载线程数（默认 2）
- `--data_dir`：数据下载目录（默认 `./data`）

## 五、测试结果如何查看
程序运行完成后，会在终端打印类似信息：

- 每轮训练/验证：
  `Epoch [01/20] Train Loss: ... Train Acc: ... Val Loss: ... Val Acc: ...`
- 最终测试：
  `Test Loss: ...`
  `Test Accuracy: ...%`

并自动生成：
- `outputs/best_cifar10_cnn.pth`（最佳模型）
- `outputs/training_curve.png`（训练曲线）
- `outputs/test_confusion_matrix.png`（测试混淆矩阵）

## 六、建议截图内容
请在 `screenshots/` 文件夹中保存以下截图（自行运行后截图）：
1. **训练过程截图**：包含多轮 Epoch 日志输出。
2. **测试结果截图**：包含最终 `Test Loss` 与 `Test Accuracy` 输出。
3. （可选）`outputs/training_curve.png` 与 `outputs/test_confusion_matrix.png` 的图片查看界面截图。

## 七、最终提交建议文件
- `cifar10_cnn_train_test.py`（完整原始代码）
- `README.md`
- `requirements.txt`
- `screenshots/` 中的训练与测试截图

> 注意：
> - 不要提交 CIFAR-10 数据集本体（`data/` 目录）。
> - 不要提交大型模型与输出图片（按 `.gitignore` 规则忽略）。
