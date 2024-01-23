# rpmol

Python package for the conversion and manipulation of chemical data.

## Installation

You can install the package using pip:

```bash
pip install rpmol

### Usage

```bash

rpmol file.xlsx -> transforms an Excel file - containing molecule identifiers (code, name) in the first column and SMILES codes in the second column - into an sdf file.

rpmol file.sdf -> transforms an sdf file - containing molecule identifiers (code, name) and SMILES codes - into an xlsx file.