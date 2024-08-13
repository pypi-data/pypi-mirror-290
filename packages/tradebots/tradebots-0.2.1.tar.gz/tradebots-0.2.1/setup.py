from setuptools import setup, find_packages

setup(
    name="tradebots",
    version="0.2.1",
    author="Kryzhanovskiy Maxim",
    author_email="kryzhanovskiymax@mail.ru",
    description="Package for building tradebots",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/your_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'typing==3.7.4.3'
    ]
)