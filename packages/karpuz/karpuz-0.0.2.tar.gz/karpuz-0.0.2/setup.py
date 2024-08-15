from setuptools import setup, find_packages

setup(
    name="karpuz",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "karpuzu-kez = karpuz:hello"
        ]
    }
)
