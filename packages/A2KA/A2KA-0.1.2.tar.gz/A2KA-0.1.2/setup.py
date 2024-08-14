from setuptools import setup, find_packages

setup(
    name="A2KA",  # 包的名字
    version="0.1.2",  # 版本号
    author="Yifan Li",
    author_email="2543179079@qq.com",
    description="Attention to Key Area, a plug and play interpretable network.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Dsadd4/NLSExplorer_1.0/",  # 项目的主页链接
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
