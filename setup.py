from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="issuescan",
    version="1.0.0",
    description="AI-powered GitHub issue summarizer — instant triage for any issue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TheChyeahhh",
    url="https://github.com/TheChyeahhh/issuescan",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "anthropic>=0.40.0",
        "openai>=1.50.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "issuescan=issuescan.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
)
