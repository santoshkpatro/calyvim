from setuptools import setup, find_packages

setup(
    name="calyvim",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer==0.16.0",
        "uvicorn==0.34.3",
        "starlette==0.47.0",
        "Jinja2==3.1.6",
    ],
    entry_points={
        "console_scripts": [
            "calyvim = calyvim.cli:cli",
        ],
    },
)
