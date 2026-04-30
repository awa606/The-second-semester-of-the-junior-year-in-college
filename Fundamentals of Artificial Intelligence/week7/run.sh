#!/bin/bash
#SBATCH --job-name=my_pytorch_job     # 作业名称
#SBATCH --partition=gpu_a800          # 分区名称（根据超算配置调整）
#SBATCH --nodes=1                      # 节点数
#SBATCH --ntasks-per-node=1            # 每个节点的任务数
#SBATCH --cpus-per-task=6              # 每个任务的CPU核心数
#SBATCH --gpus=1                       # GPU数量
#SBATCH --output=job_%j.out            # 输出日志文件
#SBATCH --error=job_%j.err             # 错误日志文件

# 加载必要的模块（根据超算环境调整）
# module load cuda/11.8
# module load cudnn/8.6.0

START_TIME=$(date +%s)
echo "作业开始时间: $(date '+%Y-%m-%d %H:%M:%S')"


# 运行Python脚本
# python main_class_hunxiao.py


# 记录结束时间并计算运行时间
END_TIME=$(date +%s)
ELAPSED_TIME=$((END_TIME - START_TIME))

ELAPSED_READABLE=$(printf "%02d:%02d:%02d" $((ELAPSED_TIME/3600)) $((ELAPSED_TIME%3600/60)) $((ELAPSED_TIME%60)))

echo "作业结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "总运行时间: $ELAPSED_READABLE (HH:MM:SS)"

echo "结束时间: $(date)"
echo "作业完成"