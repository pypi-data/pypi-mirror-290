from setuptools import setup, find_packages
from pathlib import Path

# Lese den Inhalt der README.md-Datei
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='csv_analyzer_extended',
    version='1.2',
    packages=find_packages(),
    description='A CSV analyzer tool with extended filtering and analysis capabilities',
    long_description=long_description,  # Füge die lange Beschreibung hinzu
    long_description_content_type='text/markdown',  # Gib das Format der langen Beschreibung an
    author='Ralf Krümmel',
    author_email='ralf.kruemmel+python@outlook.de',
    license='MIT',
    install_requires=[],
)
