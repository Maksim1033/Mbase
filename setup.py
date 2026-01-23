from setuptools import setup, find_packages

# На время разработки ( Version<1.0.0 ), данный файл будет использоваться.

setup(
    name="mbase",
    version="0.1.3.1",
    description="Удобная библиотека с базовыми инструментами",
    author="Maksim1033",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.1",
)