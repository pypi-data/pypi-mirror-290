from setuptools import setup, find_packages

setup(
    name="sinopsis-ai",
    version="0.3.0", 
    author="Sinopsis Data, LLC", 
    author_email="hello@sinopsisai.com",
    description="A Python SDK for Sinopsis AI",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown", 
    url="https://github.com/sinopsis-ai/sinopsis-ai-sdk", 
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
    python_requires='>=3.6',
    install_requires=[
        "boto3==1.24.28"
    ]
)