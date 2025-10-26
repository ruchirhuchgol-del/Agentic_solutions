"""
Setup script for DevSecOps Deployment Gatekeeper.
"""
from setuptools import setup, find_packages

# Read the contents of README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="devops-deployment-security-gate",
    version="1.0.0",
    author="DevSecOps Team",
    author_email="security@example.com",
    description="DevSecOps Deployment Gatekeeper - Automated Security Checks for CI/CD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/devops-deployment-security-gate",
    project_urls={
        "Bug Tracker": "https://github.com/example/devops-deployment-security-gate/issues",
        "Documentation": "https://github.com/example/devops-deployment-security-gate/blob/main/README.md",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Quality Assurance",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src", include=["devops_deployment_security_gate", "devops_deployment_security_gate.*"]),
    python_requires=">=3.10,<3.14",
    install_requires=[
        "crewai>=0.177.0,<1.0.0",
        "crewai-tools>=0.177.0,<1.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "pydantic-settings>=2.0.0,<3.0.0",
        "python-dotenv>=0.19.0",
        "PyYAML>=5.4.1",
        "requests>=2.25.1",
    ],
    entry_points={
        "console_scripts": [
            "devsecops-gate=devops_deployment_security_gate.main:main",
            "security-gate=devops_deployment_security_gate.core.orchestrator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "devops_deployment_security_gate": ["config/*.yaml", "config/*.yml"],
    },
)