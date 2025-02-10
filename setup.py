from setuptools import setup, find_packages

setup(
    name="ai_fashion_classifier",
    version="0.1.0",
    description="AI-powered clothing image classifier using OpenAI's vision models",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.61.0",
        "Pillow>=11.0.0",
        "pydantic>=2.10.0",
        "pydantic-settings>=2.7.0",
        "click>=8.1.0",
        "python-dotenv>=1.0.0",
        "aiofiles>=24.1.0",
        "asyncio>=3.4.3"
    ],
    entry_points={
        'console_scripts': [
            'ai-fc=ai_fashion_classifier.__main__:main',
        ],
    },
)
