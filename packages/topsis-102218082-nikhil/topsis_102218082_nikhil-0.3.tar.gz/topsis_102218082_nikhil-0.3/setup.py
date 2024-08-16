from setuptools import setup, find_packages

setup(
    name='topsis-102218082-nikhil',
    version='0.3',
    author='Nikhil Gupta',
    author_email='nikhilgupta8235@gmail.com',
    description='A Python package for TOPSIS method',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'topsis-102218082-nikhil = topsis_102218082_nikhil.topsis:main'
        ],
    },
    install_requires=[
        'numpy',
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

