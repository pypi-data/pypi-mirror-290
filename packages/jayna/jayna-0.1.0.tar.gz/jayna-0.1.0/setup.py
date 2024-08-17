from setuptools import setup, find_packages

setup(
    name="jayna",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        # List your package dependencies here
        # In this case, we don't have any external dependencies
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
    author="Jayna",
    author_email="jaynahuang@gmail.com",
    description="A jayna package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jhuang1723/jayna",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)