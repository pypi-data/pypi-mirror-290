from setuptools import setup, find_packages

with open("readme.md", "r") as f:
    description = f.read()

setup(
    name="karpuz",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "karpuzu-kez = karpuz:hello"
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown"
)
