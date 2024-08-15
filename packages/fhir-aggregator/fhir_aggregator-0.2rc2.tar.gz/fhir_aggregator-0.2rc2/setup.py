from setuptools import setup, find_packages

# Step 1: Read requirements.txt for dependencies
with open('requirements.txt') as f:
    required = f.read().splitlines()

# Step 2: Read README.md for the long description
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Step 3: Define the setup
setup(
    name='fhir-aggregator',
    version='0.2rc2',
    packages=find_packages(),
    install_requires=required,
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'fhir-aggregator=fhir_aggregator.cli:cli',
        ],
    },
    # Add more package metadata as needed
)
