from setuptools import setup, find_packages

setup(
    name='Atrajit',  # Project name
    version='1.0',  # Initial version
    description='A Python package that includes Cryptography, Maths, and Telebot modules',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='atrajit-sarkar',
    author_email='atrajit.sarkar@gmail.com',
    url='https://github.com/atrajit-sarkar/Atr',  # Update with your repository URL
    packages=find_packages(),  # Automatically find packages in the project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version required
    install_requires=[
        # List your dependencies here
        'cryptography>=43.0.0',
    ],
)
