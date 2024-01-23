from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="topsis_102103043",
    version="1.1.0",
    description="A Python package to rank ML models/choices using topsis technique",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/iosaman503/topsis-package.git",
    author="Aman Verma",
    author_email="amanverma24680@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis_102103043"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "topsis-package=topsis_102103043.__init__:main",
        ]
    },
)
