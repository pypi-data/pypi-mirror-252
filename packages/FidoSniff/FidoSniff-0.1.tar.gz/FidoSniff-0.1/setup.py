from setuptools import setup, find_packages

setup(
    name='FidoSniff',
    description='Libreria Fido Sniff para Calidad de Datos',    
    version='0.1',
    packages=find_packages(),
    author='Enzo Ipanaque',
    author_email='eipanaquep@pucp.edu.pe',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pyspark',
    ],
    entry_points={
        'console_scripts': [
            'mi_libreria = mi_libreria.main:main',
        ],
    },
    py_modules=['src'],
    zip_safe=False
)