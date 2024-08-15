from setuptools import setup, find_packages

setup(
    name="apitelev", 
    version="0.2",
    author="Ngọc An",
    author_email="gcvinhheo113@gmail.com",
    description="Thả Icon Tin Nhắn và reply",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
    ],
)