from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pop_jetson', 
    version='0.0.6',
    author="c.h.min",
    author_email="lab2@hanback.co.kr",
    description="AIoT AI library for pop",
    install_requires=[
        "gdown",
        "pycuda",
        "numpy>=1.19.5, <=1.23.5",
        "onnx==1.9.0; python_version=='3.6'",
        "onnx>=1.12.0; python_version=='3.8'",
    ],
    long_description=long_description,
    python_requires='>=3.6',
    long_description_content_type="text/markdown",
    packages= find_packages(exclude = ['docs', '__pycache__/']),
    include_package_data=True,   
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
