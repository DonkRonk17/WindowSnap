#!/usr/bin/env python3
"""
WindowSnap Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="windowsnap",
    version="1.0.0",
    author="Team Brain",
    author_email="logan@metaphysicsandcomputing.com",
    description="Smart Window Layout Manager - Save and restore window positions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/WindowSnap",
    py_modules=["windowsnap", "windowsnap_tray"],
    python_requires=">=3.7",
    install_requires=[
        "psutil>=5.9.0",
    ],
    extras_require={
        "windows": ["pywin32>=305"],
        "macos": ["pyobjc-framework-Quartz>=9.0"],
        "gui": ["PyQt5>=5.15.0"],
    },
    entry_points={
        "console_scripts": [
            "windowsnap=windowsnap:main",
            "windowsnap-tray=windowsnap_tray:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment :: Window Managers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    keywords="window manager layout desktop productivity multi-monitor",
)
