from setuptools import find_packages, setup

setup(
    name="AdI_bot",
    version="0.1.0",
    author="Adiba Arooj",
    author_email="adibaarooj@gmail.com",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "ollama",
        "pandas",
        "numpy",
        "scikit-learn",
        "nltk",
        "spacy",
        "transformers",
        "torch",
        "tensorflow",
        "flask",
        "flask-cors",
        "python-dotenv"
    ]
)