from pathlib import Path

from setuptools import find_packages, setup


setup(
    name="oxgpt",
    version="0.1.0",
    description="A local terminal AI assistant powered by Ollama.",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.9",
    entry_points={"console_scripts": ["oxgpt=oxgpt.cli:main"]},
)
