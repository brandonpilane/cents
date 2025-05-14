from setuptools import setup, find_packages

setup(
    name="cents",
    version="0.0.0",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "cents=cents.cli:cli",
        ],
    },
)
