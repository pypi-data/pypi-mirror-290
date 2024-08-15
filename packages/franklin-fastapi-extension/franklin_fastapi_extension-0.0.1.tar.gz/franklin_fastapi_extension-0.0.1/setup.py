from setuptools import setup, find_packages

setup(
    name="franklin_fastapi_extension",
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "mysql-connector-python"
    ],
    include_package_data=True,
    description="This is a FastAPI Extension to simplify the creation process of APIS",
    author="Franklin Neves Filho",
    url="https://github.com/franklinnevesfilho/SimpleAPI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8"
)
