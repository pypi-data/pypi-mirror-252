from setuptools import setup, find_packages

setup(
    name="abdur-test-utilities",
    version="0.3",
    packages=find_packages(),
    author="Your Name",
    author_email="your.email@example.com",
    description="A small utility for email validation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "pandas>=1.2.4",
    ],
)
