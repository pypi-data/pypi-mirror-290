import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="barstools",
    version="0.0.1",
    author="-T.K.-",
    author_email="t_k_233@outlook.email",
    description="Useful utilities for UC Berkeley Architecture Research (BAR) projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ucb-bar/barstools",
    project_urls={
        
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)