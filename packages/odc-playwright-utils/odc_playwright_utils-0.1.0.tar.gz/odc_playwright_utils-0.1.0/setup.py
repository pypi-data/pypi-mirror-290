from setuptools import setup, find_packages

setup(
    name="odc_playwright_utils",
    version="0.1.0",
    description="A set of utility functions for Playwright-based UI automation",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="qym00725@163.com",
    packages=find_packages(),
    install_requires=[
        'playwright==1.45.1',  # 依赖Playwright 1.45.1版本
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)