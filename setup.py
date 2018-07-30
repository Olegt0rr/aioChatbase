import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aioChatbase",
    version="0.0.8",
    author="Oleg Abramov",
    author_email="1282524@gmail.com",
    description="Asyncio Chatbase API library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Olegt0rr/aioChatbase",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
    ),
)
