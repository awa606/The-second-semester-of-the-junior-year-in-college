mkdir -p D:/python_projects/deep_learning_platform
cd D:/python_projects/deep_learning_platform

# 创建所有目录
mkdir -p {configs,data,models,core,utils,scripts,tests,experiments}

# 创建 __init__.py
touch models/__init__.py
touch data/__init__.py
touch core/__init__.py
touch utils/__init__.py

# 创建其他文件
touch configs/{base,train,test}.yaml
touch data/{datasets,transforms,loaders}.py
touch models/{base,your_model,utils}.py
touch core/{trainer,validator,metrics}.py
touch utils/{logger,checkpoint,visualization,profiler}.py
touch scripts/{train,test,debug}.py
touch tests/{test_data,test_model,test_trainer}.py
touch requirements.txt setup.py README.md