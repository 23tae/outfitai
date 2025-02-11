from setuptools import setup, find_packages

setup(
    name="outfitai",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.61.0",
        "Pillow>=11.0.0",
        "pydantic>=2.10.0",
        "pydantic-settings>=2.7.0",
        "click>=8.1.0",
        "aiofiles>=24.1.0",
        "asyncio>=3.4.3"
    ],
    entry_points={
        'console_scripts': [
            'outfitai=outfitai.__main__:main',
        ],
    },
    author="23tae",
    author_email="taehoonkim.dev@gmail.com",
    description="AI-based clothing image classification tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/23tae/outfitai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
