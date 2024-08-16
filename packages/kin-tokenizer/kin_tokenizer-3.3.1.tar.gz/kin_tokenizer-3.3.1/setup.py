from setuptools import setup, find_packages

with open('README.md') as f:
    description = f.read()


setup(
    name='kin_tokenizer',
    version='3.3.1',
    author='Schadrack Niyibizi',
    author_email='niyibizischadrack@gmail.com',
    description='Kinyarwanda tokenizer for encoding and decoding Kinyarwanda language text',
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nschadrack/Kin-Tokenizer',
    packages=find_packages(),
    keywords="Tokenizer, Kinyarwanda, KinGPT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        "regex>=2024.7.24"
    ],
    package_data={
        'kin_tokenizer': ['data/*'],
    },
    include_package_data=True,
)