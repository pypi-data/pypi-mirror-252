from setuptools import setup, find_packages
import os

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="async_foaas",
    version="0.4.0",
    description="Fuck Off As A Service",
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    license="MIT",
    url="https://github.com/alexraskin/foaas-python",
    author="Alex Raskin",
    author_email="root@alexraskin.com",
    py_modules=["async_foaas"],
    install_requires=["httpx", "async-property"],
    packages=find_packages(),
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
    ),
)
