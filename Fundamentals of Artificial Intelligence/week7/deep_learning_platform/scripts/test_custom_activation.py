import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.layers import *

# 测试自定义激活函数
def test_custom_activation():
    """测试自定义激活函数"""
    print("\n2. 自定义激活函数测试")
    print("=" * 60)

    # 创建激活函数
    act1 = CustomActivation(alpha=0.2)
    act2 = SwishActivation(beta=1.0, trainable=True)

    print(f"自定义激活函数1: {act1}")
    print(f"Swish激活函数: {act2}")

    # 测试前向传播
    x = torch.linspace(-3, 3, 10)
    y1 = act1(x)
    y2 = act2(x)

    print(f"\n输入: {x}")
    print(f"自定义激活输出: {y1}")
    print(f"Swish激活输出: {y2}")

    # 可视化
    import matplotlib.pyplot as plt

    x_vis = torch.linspace(-3, 3, 100)
    y_custom = act1(x_vis)
    y_swish = act2(x_vis)

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(x_vis.numpy(), y_custom.detach().numpy(), 'b-', linewidth=2)
    plt.title('Custom Activation (alpha=0.2)')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(x_vis.numpy(), y_swish.detach().numpy(), 'r-', linewidth=2)
    plt.title('Swish Activation (beta=1.0)')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('custom_activations.png', dpi=150, bbox_inches='tight')
    plt.show()

    print("\n激活函数可视化已保存为 custom_activations.png")

    return act1, act2

if __name__ == "__main__":
    act1, act2 = test_custom_activation()