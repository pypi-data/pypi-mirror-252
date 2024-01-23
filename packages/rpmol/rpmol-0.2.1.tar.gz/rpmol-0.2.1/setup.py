from setuptools import setup, find_packages

setup(
    name='rpmol',
    version='0.2.1',
    packages=find_packages(),
    description='Paquete para la conversión y manipulación de datos estructurales.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rubén Prieto-Díaz',
    author_email='ruben.prietodiaz@icm.uu.se',
    url='https://github.com/usuario/rpmol',
    license='MIT',
    entry_points={
        'console_scripts': [
            'rpmol=rpmol.rpmol:main',  # Ajustado para apuntar a la función main en rpmol.py
        ],
    },
    install_requires=[
        'pandas',
        'rdkit',
        'openpyxl',
        'reportlab'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
    ],
)
