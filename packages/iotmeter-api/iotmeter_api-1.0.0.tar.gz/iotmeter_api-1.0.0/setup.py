from setuptools import setup, find_packages

setup(
    name="iotmeter_api",
    version="1.0.0",
    description="A Python library to interact with IoT Meter devices",
    author="lipic",
    author_email="tvoje.email@example.com",
    url="https://github.com/lipic/iotmeter_api",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
