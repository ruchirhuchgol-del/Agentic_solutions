from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="autonomous-trading-crew",
    version="0.1.0",
    author="Your Name",
    author_email="you@example.com",
    description="An AI-powered multi-agent system for comprehensive stock market analysis and trading recommendations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/autonomous-trading-crew",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10,<3.14",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "autonomous-trading-crew=autonomous_trading_crew.main:run",
            "atc-cli=autonomous_trading_crew.ui.cli:main",
        ],
    },
)