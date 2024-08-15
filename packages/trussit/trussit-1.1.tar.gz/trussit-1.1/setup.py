from setuptools import setup, find_packages

setup(
    name='trussit',
    version='1.1',
    author='kunalgokhe',
    author_email='kunalgokhe@gmail.com',
    long_description=open('README.md').read(),
    keywords=['Truss','Beam','FEA','Deformation'],
    packages=find_packages(),
install_requires=[
        'numpy<2',
        'customtkinter<=5.2.2',
        'matplotlib<=3.9.1',
        'pylatex<=1.4.2',
        'pybind11<=2.12',
    ],
classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'trussit = trussit.main:GUI',
        ]
    }
)