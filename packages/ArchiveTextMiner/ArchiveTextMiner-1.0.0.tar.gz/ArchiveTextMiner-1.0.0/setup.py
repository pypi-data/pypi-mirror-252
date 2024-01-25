from setuptools import setup, find_packages

setup(
    name='ArchiveTextMiner',
    version='1.0.0',
    description='Transform textual information to structured metadata in MDTO-format.',
    author='Muriël Valckx',
    author_email='my.valckx@zeeland.nl',
    url='https://github.com/zeeuws-archief/ArchiveTextMiner',
    packages=find_packages(),
    install_requires=[
        'langdetect',
        'PyPDF2',
        'python-magic',
        'transformers',
        'scikit-learn',
    ],
    license='EUPL',
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved",
    "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'ArchiveTextMiner=main:main',  
        ],
    },
)



