from setuptools import setup, find_packages

# Read the contents of your README file
with open("C:\\Users\\danie\\PycharmProjects\\finch2\\Finch\\README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='finch-genetics',
    version='3.0.10',
    packages=find_packages(),
    author="Daniel Losey",
    license="MIT",
    install_requires=[
        "torch",
        "transformers",
        "diffusers",
        "numpy",
        "matplotlib",
        "typing_extensions",
        "accelerate"
    ],
    # Include the README content as the long description
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify the content type

    # Add project URLs, including GitHub repository
    url="https://github.com/dadukhankevin/Finch",
    project_urls={
        "Source": "https://github.com/dadukhankevin/Finch",
    },
)
