import os
from PIL import Image
import gzip
import numpy as np
import struct
from torch.utils.data import Dataset
from torchvision import transforms
from data.transforms import BasicTransforms
import matplotlib.pyplot as plt

class SimpleImageDataset(Dataset):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.image_paths = []  # 存储图片路径
        self.labels = []  # 存储标签
        self._load_images()  # 加载数据

    def _load_images(self):
        # 1. 获取所有类别文件夹
        # 2. 遍历每个文件夹
        # 3. 收集图片路径和标签
        raise NotImplementedError

    def __len__(self):
        return len(self.image_paths)  # 必须实现

    def __getitem__(self, idx):
        # 1. 根据idx获取图片路径
        # 2. 加载图片
        # 3. 返回(图片, 标签)  # 必须实现
        raise NotImplementedError


class MNIST(SimpleImageDataset):
    def __init__(self, root_dir, is_train=True):
        self.root_dir = root_dir
        self.is_train = is_train
        self._load_images()

    def _load_images(self):
        if self.is_train:
            images_file = os.path.join(self.root_dir, 'train-images-idx3-ubyte')
            labels_file = os.path.join(self.root_dir, 'train-labels-idx1-ubyte')
        else:
            images_file = os.path.join(self.root_dir, 't10k-images-idx3-ubyte')
            labels_file = os.path.join(self.root_dir, 't10k-labels-idx1-ubyte')

            # 检查文件是否存在
        if not os.path.exists(images_file):
            # 尝试 .gz 文件
            images_file_gz = images_file + '.gz'
            if os.path.exists(images_file_gz):
                with gzip.open(images_file_gz, 'rb') as f_in:
                    with open(images_file, 'wb') as f_out:
                        f_out.write(f_in.read())
            else:
                raise FileNotFoundError(f"找不到 MNIST 数据文件: {images_file}")

        if not os.path.exists(labels_file):
            labels_file_gz = labels_file + '.gz'
            if os.path.exists(labels_file_gz):
                with gzip.open(labels_file_gz, 'rb') as f_in:
                    with open(labels_file, 'wb') as f_out:
                        f_out.write(f_in.read())
            else:
                raise FileNotFoundError(f"找不到 MNIST 标签文件: {labels_file}")

            # 读取图像文件
        with open(images_file, 'rb') as f:
            # 读取文件头
            magic, num_images, rows, cols = struct.unpack('>IIII', f.read(16))

            if magic != 2051:  # MNIST 图像文件魔数
                raise ValueError(f'非法的 MNIST 图像文件: {images_file}')

            print(f"加载 {num_images} 张图片，尺寸: {rows}x{cols}")

            # 读取所有图像数据
            image_data = np.frombuffer(f.read(), dtype=np.uint8)
            image_data = image_data.reshape(num_images, rows, cols)

            # 转换为 PIL 图像列表
            self.images = []
            for i in range(num_images):
                img = Image.fromarray(image_data[i], mode='L')
                self.images.append(img)

            # 读取标签文件
        with open(labels_file, 'rb') as f:
            # 读取文件头
            magic, num_labels = struct.unpack('>II', f.read(8))

            if magic != 2049:  # MNIST 标签文件魔数
                raise ValueError(f'非法的 MNIST 标签文件: {labels_file}')

            if num_images != num_labels:
                raise ValueError(f'图片数量({num_images})和标签数量({num_labels})不匹配')

            # 读取所有标签
            self.labels = list(np.frombuffer(f.read(), dtype=np.uint8))

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        return self.images[idx], self.labels[idx]


class MNIST_1(SimpleImageDataset):
    def __init__(self, root_dir, is_train=True):
        self.root_dir = root_dir
        self.is_train = is_train
        self._load_images()

    def _load_images(self):
        if self.is_train:
            images_file = os.path.join(self.root_dir, 'train-images-idx3-ubyte')
            labels_file = os.path.join(self.root_dir, 'train-labels-idx1-ubyte')
        else:
            images_file = os.path.join(self.root_dir, 't10k-images-idx3-ubyte')
            labels_file = os.path.join(self.root_dir, 't10k-labels-idx1-ubyte')

            # 检查文件是否存在
        if not os.path.exists(images_file):
            # 尝试 .gz 文件
            images_file_gz = images_file + '.gz'
            if os.path.exists(images_file_gz):
                with gzip.open(images_file_gz, 'rb') as f_in:
                    with open(images_file, 'wb') as f_out:
                        f_out.write(f_in.read())
            else:
                raise FileNotFoundError(f"找不到 MNIST 数据文件: {images_file}")

        if not os.path.exists(labels_file):
            labels_file_gz = labels_file + '.gz'
            if os.path.exists(labels_file_gz):
                with gzip.open(labels_file_gz, 'rb') as f_in:
                    with open(labels_file, 'wb') as f_out:
                        f_out.write(f_in.read())
            else:
                raise FileNotFoundError(f"找不到 MNIST 标签文件: {labels_file}")

            # 读取图像文件
        with open(images_file, 'rb') as f:
            # 读取文件头
            magic, num_images, rows, cols = struct.unpack('>IIII', f.read(16))

            if magic != 2051:  # MNIST 图像文件魔数
                raise ValueError(f'非法的 MNIST 图像文件: {images_file}')

            print(f"加载 {num_images} 张图片，尺寸: {rows}x{cols}")

            # 读取所有图像数据
            image_data = np.frombuffer(f.read(), dtype=np.uint8)
            image_data = image_data.reshape(num_images, rows, cols)

            # 转换为 PIL 图像列表
            self.images = []
            for i in range(num_images):
                img = Image.fromarray(image_data[i], mode='L')
                self.images.append(img)

            # 读取标签文件
        with open(labels_file, 'rb') as f:
            # 读取文件头
            magic, num_labels = struct.unpack('>II', f.read(8))

            if magic != 2049:  # MNIST 标签文件魔数
                raise ValueError(f'非法的 MNIST 标签文件: {labels_file}')

            if num_images != num_labels:
                raise ValueError(f'图片数量({num_images})和标签数量({num_labels})不匹配')

            # 读取所有标签
            self.labels = list(np.frombuffer(f.read(), dtype=np.uint8))

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        to_tensor = transforms.ToTensor()
        return to_tensor(self.images[idx]), self.labels[idx]


class MNIST_2(SimpleImageDataset):
    def __init__(self, root_dir, image_size, mean_value, std_value, is_train=True):
        self.root_dir = root_dir
        self.is_train = is_train
        self.transform = BasicTransforms.get_transform(image_size, mean_value, std_value)
        self._load_images()

    def _load_images(self):
        if self.is_train:
            images_file = os.path.join(self.root_dir, 'train-images-idx3-ubyte')
            labels_file = os.path.join(self.root_dir, 'train-labels-idx1-ubyte')
        else:
            images_file = os.path.join(self.root_dir, 't10k-images-idx3-ubyte')
            labels_file = os.path.join(self.root_dir, 't10k-labels-idx1-ubyte')

            # 检查文件是否存在
        if not os.path.exists(images_file):
            # 尝试 .gz 文件
            images_file_gz = images_file + '.gz'
            if os.path.exists(images_file_gz):
                with gzip.open(images_file_gz, 'rb') as f_in:
                    with open(images_file, 'wb') as f_out:
                        f_out.write(f_in.read())
            else:
                raise FileNotFoundError(f"找不到 MNIST 数据文件: {images_file}")

        if not os.path.exists(labels_file):
            labels_file_gz = labels_file + '.gz'
            if os.path.exists(labels_file_gz):
                with gzip.open(labels_file_gz, 'rb') as f_in:
                    with open(labels_file, 'wb') as f_out:
                        f_out.write(f_in.read())
            else:
                raise FileNotFoundError(f"找不到 MNIST 标签文件: {labels_file}")

            # 读取图像文件
        with open(images_file, 'rb') as f:
            # 读取文件头
            magic, num_images, rows, cols = struct.unpack('>IIII', f.read(16))

            if magic != 2051:  # MNIST 图像文件魔数
                raise ValueError(f'非法的 MNIST 图像文件: {images_file}')

            print(f"加载 {num_images} 张图片，尺寸: {rows}x{cols}")

            # 读取所有图像数据
            image_data = np.frombuffer(f.read(), dtype=np.uint8)
            image_data = image_data.reshape(num_images, rows, cols)

            # 转换为 PIL 图像列表
            self.images = []
            for i in range(num_images):
                img = Image.fromarray(image_data[i], mode='L')
                self.images.append(img)

            # 读取标签文件
        with open(labels_file, 'rb') as f:
            # 读取文件头
            magic, num_labels = struct.unpack('>II', f.read(8))

            if magic != 2049:  # MNIST 标签文件魔数
                raise ValueError(f'非法的 MNIST 标签文件: {labels_file}')

            if num_images != num_labels:
                raise ValueError(f'图片数量({num_images})和标签数量({num_labels})不匹配')

            # 读取所有标签
            self.labels = list(np.frombuffer(f.read(), dtype=np.uint8))

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        self.images[idx] = self.transform(self.images[idx])
        return self.images[idx], self.labels[idx]


class MNIST_3(SimpleImageDataset):
    def __init__(self, root_dir, n_train=10000, is_train=True):
        self.root_dir = root_dir
        self.n_train = n_train
        self.is_train = is_train
        self._load_images()

    def _load_images(self):
        if self.is_train:
            images_file = os.path.join(self.root_dir, 'train-images-idx3-ubyte')
            labels_file = os.path.join(self.root_dir, 'train-labels-idx1-ubyte')
        else:
            images_file = os.path.join(self.root_dir, 't10k-images-idx3-ubyte')
            labels_file = os.path.join(self.root_dir, 't10k-labels-idx1-ubyte')

            # 检查文件是否存在
        if not os.path.exists(images_file):
            # 尝试 .gz 文件
            images_file_gz = images_file + '.gz'
            if os.path.exists(images_file_gz):
                with gzip.open(images_file_gz, 'rb') as f_in:
                    with open(images_file, 'wb') as f_out:
                        f_out.write(f_in.read())
            else:
                raise FileNotFoundError(f"找不到 MNIST 数据文件: {images_file}")

        if not os.path.exists(labels_file):
            labels_file_gz = labels_file + '.gz'
            if os.path.exists(labels_file_gz):
                with gzip.open(labels_file_gz, 'rb') as f_in:
                    with open(labels_file, 'wb') as f_out:
                        f_out.write(f_in.read())
            else:
                raise FileNotFoundError(f"找不到 MNIST 标签文件: {labels_file}")

            # 读取图像文件
        with open(images_file, 'rb') as f:
            # 读取文件头
            magic, num_images, rows, cols = struct.unpack('>IIII', f.read(16))

            if magic != 2051:  # MNIST 图像文件魔数
                raise ValueError(f'非法的 MNIST 图像文件: {images_file}')

            print(f"加载 {num_images} 张图片，尺寸: {rows}x{cols}")

            # 读取所有图像数据
            image_data = np.frombuffer(f.read(), dtype=np.uint8)
            image_data = image_data.reshape(num_images, rows, cols)

            # 转换为 PIL 图像列表
            self.images = []
            for i in range(num_images):
                img = Image.fromarray(image_data[i], mode='L')
                self.images.append(img)

            # 读取标签文件
        with open(labels_file, 'rb') as f:
            # 读取文件头
            magic, num_labels = struct.unpack('>II', f.read(8))

            if magic != 2049:  # MNIST 标签文件魔数
                raise ValueError(f'非法的 MNIST 标签文件: {labels_file}')

            if num_images != num_labels:
                raise ValueError(f'图片数量({num_images})和标签数量({num_labels})不匹配')

            # 读取所有标签
            self.labels = list(np.frombuffer(f.read(), dtype=np.uint8))
        if self.is_train:
            self.images = self.images[:self.n_train]
            self.labels = self.labels[:self.n_train]

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        to_tensor = transforms.ToTensor()
        return to_tensor(self.images[idx]), self.labels[idx]