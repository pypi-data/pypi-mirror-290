# TorchCat 🐱

# 简介

TorchCat 是用于封装 PyTorch 模型的工具

提供以下功能：

- 加载数据
- 封装模型
- 训练模型
- 评估模型
- 记录日志

# 加载数据

使用 `torchcat.ImageFolder` 用于加载图片数据集

```python
# 图像预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# 加载数据集
train_set = torchcat.ImageFolder(path='train-image', transform=data_transorms, one_hot=True)
test_set = torchcat.ImageFolder(path='test-image', transform=data_transorms, one_hot=True)

# 创建数据加载器
train_loader = torch.utils.data.DataLoader(train_set, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=64, shuffle=True)
```

| 参数      | 说明                                |
| --------- | ----------------------------------- |
| path      | 数据集路径                          |
| transform | 图像预处理方案                      |
| one_hot   | 是否进行 One-Hot 编码（默认 False） |

# 封装模型

使用 `torchcat.Cat` 封装你的模型。如果不进行训练，也可以忽略 `loss_fn`、`optimizer` 参数

```python
net = nn.Sequential(
    nn.Flatten(),
    nn.Linear(28*28, 128),
    nn.ReLU(),
    nn.Linear(128, 10),
).cuda()

net = torchcat.Cat(model=net,
                   loss_fn=nn.CrossEntropyLoss(),
                   optimizer=torch.optim.Adam(net.parameters()),
                   metrics=[torchcat.metrics.CrossEntropyAccuracy()])
```

| 参数      | 说明     |
| --------- | -------- |
| model     | 你的模型 |
| loss_fn   | 损失函数 |
| optimizer | 优化器   |
| metrics   | 评估指标 |

## 查看结构

在封装模型后，可使用 `net.summary()`，可以查看模型的结构。`input_size` 参数需填写模型的输入形状，如：`net.summary(1, 28, 28)`

## 训练模型

使用 `net.train()`，可以开始模型的训练。训练结束后会返回训练日志

```python
log = net.train(epochs=10, train_set=train_loader, valid_set=test_loader)
```

`log` 记录了训练时的日志，包含 loss 和 metrics 所定义的指标

| 参数      | 说明                |
| --------- | ------------------- |
| epochs    | 训练轮次            |
| train_set | 训练集              |
| valid_set | 验证集（默认 None） |

## 评估模型

使用 `net.valid(valid_set, show=True, train=False)`，能够验证模型在给定验证集上的性能，包括损失值、评估指标。验证后模型将保留推理模式

| 参数      | 说明                                          |
| --------- | --------------------------------------------- |
| valid_set | 验证集                                        |
| show      | 是否输出验证集上损失值、评估指标（默认 True） |
| train     | 验证后是否将模型切换为训练模式（默认 False）  |

# 其他

## 模型推理

使用 `net(x)` 执行模型前向推理

## 切换计算设备

TorchCat 提供了方法 `to_cpu()`、`to_cuda()` 用于切换计算设备（CPU 或 GPU🚀）

## 检查模型当前模式

使用 `training` 方法，查看模型当前是否处于训练模式。返回 `True` 表示处于训练模式，`False` 表示处于推理模式
