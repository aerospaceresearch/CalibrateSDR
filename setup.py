import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setuptools.setup(
    name="CalibrateSDR",  # Replace with your own username
    version="0.0.1",
    license="MIT",
    author="aerospaceresearch.net community",
    author_email="calibratesdr@aerospaceresearch.net",
    description="A small package for calibrating software defined radios (SDR)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aerospaceresearch/CalibrateSDR",
    packages=setuptools.find_packages(),
    install_requires=[req for req in requirements if req[:2] != "# "],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
