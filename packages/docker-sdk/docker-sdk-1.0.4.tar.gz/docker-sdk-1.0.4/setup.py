from setuptools import setup, find_packages


# 从 requirements.txt 中读取依赖项
with open(file = "requirements.txt",mode = 'r',encoding = 'utf-8') as f:
    install_requires = f.read().splitlines()

setup(
    name="docker-sdk",  # 包的名称
    version="1.0.4",  # 版本号
    author="FreeTwilight",  # 作者
    author_email="zunpengyang@gmail.com",  # 作者的联系邮箱
    description="The docker python client supports asynchronous parallel access to containers.",  # 包的简单描述
    long_description=open("README.md").read(),  # 从 README.md 中读取详细描述
    long_description_content_type="text/markdown",  # README 的格式
    url="https://github.com/FreeTwilight/docker.git",  # 项目主页或仓库
    packages=find_packages(),  # 自动发现并包含包
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",  # 许可证
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Python 版本要求
    install_requires=install_requires,
)

