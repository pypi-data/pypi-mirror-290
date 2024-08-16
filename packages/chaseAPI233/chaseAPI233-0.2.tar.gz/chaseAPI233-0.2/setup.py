import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="chaseAPI233",
    version="0.2",
    author="Jinzeld",
    author_email="jinzeld@pm.me",
    description="An unofficial API for Chase Invest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/Jinzeld/chaseAPI233",
    download_url="https://github.com/Jinzeld/chaseAPI233/archive/refs/heads/main.zip",
    keywords=["CHASE", "API"],
    install_requires=["playwright", "playwright-stealth"],
    packages=["chase"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
