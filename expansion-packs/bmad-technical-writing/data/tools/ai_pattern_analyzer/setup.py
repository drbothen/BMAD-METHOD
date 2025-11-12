"""
Setup script for AI Pattern Analyzer package.

This makes the package installable via pip, allowing proper imports
throughout the codebase.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai_pattern_analyzer",
    version="5.0.0",
    author="BMad Technical Writing",
    description="Modular AI pattern analysis tool for detecting AI-generated text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"ai_pattern_analyzer": "."},
    packages=["ai_pattern_analyzer"] + ["ai_pattern_analyzer." + pkg for pkg in find_packages(exclude=["tests", "tests.*"])],
    python_requires=">=3.8",
    install_requires=[
        "marko>=2.0.0",
        "nltk>=3.8",
        "spacy>=3.7.0",
        "textstat>=0.7.3",
        "transformers>=4.35.0",
        "torch>=2.0.0",
        "scipy>=1.11.0",
        "textacy>=0.13.0",
        "numpy>=1.24.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-timeout>=2.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "analyze-ai-patterns=ai_pattern_analyzer.cli.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
