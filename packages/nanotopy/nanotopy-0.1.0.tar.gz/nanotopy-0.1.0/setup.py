from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='nanotopy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['nanorpc', 'asyncio'],
    python_requires='>=3.7',
    author='gr0vity',
    url="https://github.com/gr0vity-dev/nanotopy",
    description='async extended nano.to library for ease of use',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
