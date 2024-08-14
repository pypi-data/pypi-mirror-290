from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PercipioScrapPack",  # Nazwa twojej paczki
    version="0.0.7",  # Wersja paczki
    description="Percipio Scraper",  # Krótki opis paczki
    long_description=long_description,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "selenium",
        "webdriver_manager",
        "requests",
        "beautifulsoup4",
        "html2text",
        "markdown2",
        "pdfkit"
    ],
    entry_points={
        'console_scripts': [
            'my_package=my_package.main:main',
        ],
    },
)
