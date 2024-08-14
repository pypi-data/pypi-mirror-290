from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()


setup(
    name='tracebook',
    version='0.1.1',
    description='A comprehensive code bookkeeping package',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords=["book-keeping","visualizer"],
    author='Sujal Choudhari',
    author_email='hello@sujal.xy',
    packages=["tracebook"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)
