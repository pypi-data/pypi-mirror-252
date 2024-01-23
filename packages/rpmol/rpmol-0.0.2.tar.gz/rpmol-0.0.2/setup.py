from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Conversor between SDF an XLSX files'

# Configurando
setup(
       # el nombre debe coincidir con el nombre de la carpeta 	  
       #'modulomuysimple'
        name="rpmol", 
        version=VERSION,
        author="Rubén Prieto",
        author_email="<ruben.prietodiaz@icm.uu.se>",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas', 'rdkit', 'openpyxl', 'argparse', 'reportlab'],
        
        keywords=['python', 'sdf', 'xlsx', 'conversor'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)