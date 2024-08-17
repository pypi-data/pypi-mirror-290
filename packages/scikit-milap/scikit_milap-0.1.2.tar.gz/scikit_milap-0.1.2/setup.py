from setuptools import setup, find_packages

setup(
    name="scikit-milap",
    version="0.1.2",
    description="A wrapper around scikit learn ML models that enable you to create and use models easily.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bhaumik Talwar",
    author_email="bhaumik303@gmail.com",
    url="https://github.com/BhaumikTalwar/SCIKIT-MILAP",
    packages=find_packages(),
    install_requires=[
        "numpy==2.0.0",
        "pandas==2.2.2",
        "matplotlib==3.9.2",
        "scikit-learn==1.5.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
)
