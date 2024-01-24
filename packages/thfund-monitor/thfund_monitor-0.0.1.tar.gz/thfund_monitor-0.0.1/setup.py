import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="thfund_monitor",
    version="0.0.1",
    keywords=["monitor"],
    description="监控埋点封装",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="LiuYong",
    author_email="liuyong@thfund.com.cn",
    url="https://github.com/pypa/sampleproject",
    license="MIT License",
    packages=setuptools.find_packages(),
    install_requires=[  # 依赖包
        "flask",
        "prometheus_client",
        "os",
        "time",
        "functools",
    ],
    classifiers=[  # 其他配置项
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
