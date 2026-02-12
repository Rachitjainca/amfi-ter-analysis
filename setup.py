"""
Setup configuration for AMFI TER Analysis Package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="amfi-ter-analysis",
    version="1.0.0",
    author="Rachit Jain",
    author_email="rachit.jain@example.com",
    description="Comprehensive AMFI TER (Total Expense Ratio) analysis tool with daily automation, GitHub Actions integration, and detailed reporting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rachitjainca/amfi-ter-analysis",
    project_urls={
        "Bug Tracker": "https://github.com/Rachitjainca/amfi-ter-analysis/issues",
        "Documentation": "https://github.com/Rachitjainca/amfi-ter-analysis#readme",
        "Source Code": "https://github.com/Rachitjainca/amfi-ter-analysis.git",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "openpyxl>=3.7.0",
        "requests>=2.26.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "amfi-ter-analysis=amfi_ter_analysis.ter_github_actions:analyze_and_report",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
