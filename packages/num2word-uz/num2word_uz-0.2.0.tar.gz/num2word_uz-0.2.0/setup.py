from setuptools import setup, find_packages

setup(
    name="num2word-uz",
    version="0.2.0",
    description="Numbers to words in Uzbek language",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shoxa0707/num2word-uz",
    author="Shaxboz",
    author_email="shoxa0212@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here, e.g. 'requests', 'numpy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)