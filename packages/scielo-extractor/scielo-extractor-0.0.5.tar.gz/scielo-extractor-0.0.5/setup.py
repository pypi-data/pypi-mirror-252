from setuptools import setup, find_packages

setup(
    name="scielo-extractor",
    version='0.0.5',
    packages=find_packages(),
    description="SciELO data extractor",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    keywords="data extraction, bibliographic data, scientific literature",
    entry_points={
        'console_scripts': [
            'scielo-extractor = scielo_extractor.cli:main'
        ]
    },
    install_requires=[
        'requests', 
        'tqdm',
        'xylose',
        'pandas',
        'lxml'
    ]
)
