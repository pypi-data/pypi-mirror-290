# My Simple Package

This is a minimal example of a Python package.

# 创建虚拟环境
python -m venv myenv
# Windows
myenv\Scripts\activate
# 安装必要的包
pip install twine requests_toolbelt urllib3
# 构建包
python setup.py sdist bdist_wheel
# 安装 twine
pip install twine
# 上传PyPI
twine upload dist/*

# 重新上传包时要在dist文件夹中先删除之前的包
