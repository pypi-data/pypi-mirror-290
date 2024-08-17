from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pygsmmodem",  # 这是您的包在PyPI上的名称
    version="0.1.0",   # 版本号
    author="Relaxing",  # 作者
    author_email="benson901203@yahoo.com.tw",  # 作者邮箱
    description="A Python package for interacting with GSM modems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/130347665/pygsmmodem",  # 您的项目URL
    packages=find_packages(),
    install_requires=[
        "pyserial",  # 列出您的包的依赖
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)