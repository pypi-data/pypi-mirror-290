from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bhashan2pathtak",
    version="0.1.0",
    author="Nilesh Kumar",
    author_email="nilukush@gmail.com",
    description="A simple speech-to-text application using Wit.ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nilukush/bhashan2pathtak",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "SpeechRecognition>=3.8.1",
        "PyAudio>=0.2.11",
        "wit>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "bhashan2pathtak=bhashan2pathtak.speech_to_text:main",
        ],
    },
)