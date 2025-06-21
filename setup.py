from setuptools import setup, find_packages
from pathlib import Path

def get_version():
    version_file = Path("src/pdfm/__version__.py").read_text()
    for line in version_file.splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Version not found.")

setup(
    name="pdfm",
    version=get_version(),
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        'console_scripts': [
            'pdfm = pdfm.cli:main',
        ],
    },
    install_requires=[
        "PyPDF2",
    ],
)

# pip install --editable .