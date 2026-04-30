import torch
def autograd_demo():
    """自动微分演示"""

    # 创建需要梯度的张量
    x = torch.tensor(2.0, requires_grad=True)
    w = torch.tensor(3.0, requires_grad=True)
    b = torch.tensor(1.0, requires_grad=True)

    # 构建计算图
    y = w * x + b  # 线性变换
    z = torch.sin(y)  # 非线性激活
    loss = z ** 2  # 损失函数

    print("计算图:")
    print(f"x = {x.item()}, w = {w.item()}, b = {b.item()}")
    print(f"y = w*x + b = {y.item()}")
    print(f"z = sin(y) = {z.item()}")
    print(f"loss = z^2 = {loss.item()}")

    # 反向传播
    loss.backward()

    print("\n梯度:")
    print(f"∂loss/∂x = {x.grad.item()}")
    print(f"∂loss/∂w = {w.grad.item()}")
    print(f"∂loss/∂b = {b.grad.item()}")

    # 手动验证
    # loss = sin(w*x + b)^2
    # ∂loss/∂x = 2*sin(w*x+b)*cos(w*x+b)*w
    manual_dx = 2 * torch.sin(w * x + b) * torch.cos(w * x + b) * w
    print(f"\n手动验证 ∂loss/∂x = {manual_dx.item()}")

    return x, w, b, loss

if __name__ == "__main__":
    x, w, b, loss = autograd_demo()