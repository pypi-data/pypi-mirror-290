import setuptools

# Package metadata
NAME = "LimitlessLumos"
VERSION = "1.0.7"
DESCRIPTION = "A package providing a Flask-based server to keep Telegram bots and other scripts running indefinitely."
URL = "https://github.com/TraxDinosaur/LimitlessLumos"
AUTHOR = "TraxDinosaur"
AUTHOR_CONTACT = "https://traxdinosaur.github.io"
LICENSE = "CC-BY-SA 4.0"
KEYWORDS = ["Flask", "Telegram bot", "keep alive", "web server", "threading", "LimitlessLumos"]

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# Packages required by the project
REQUIRED_PACKAGES = [
    "Flask",
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_contact=AUTHOR_CONTACT,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
    keywords=KEYWORDS,
    install_requires=REQUIRED_PACKAGES,
    python_requires=">=3.6",
)
