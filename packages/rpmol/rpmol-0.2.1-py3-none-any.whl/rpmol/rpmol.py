import pandas as pd
from rdkit import Chem
from rdkit.Chem import Draw
import openpyxl
import argparse
import os
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def validate_excel_format(df):
    if df.columns[0].lower() in ['ID', 'code', 'molecule', 'any'] and 'smiles' in df.columns[1].lower():
        return True
    else:
        return False

def generate_molecule_images(df, image_dir, img_size=(600, 600)):
    for i, row in df.iterrows():
        smiles = str(row.iloc[1])
        ID = str(row.iloc[0])
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            img_path = os.path.join(image_dir, f'{ID}.png')
            Draw.MolToFile(mol, img_path, size=img_size)
            yield ID, img_path

def create_pdf(pdf_file, images):
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    x_margin, y_margin = 50, 50
    x_space, y_space = 60, 40
    img_display_width, img_display_height = 150, 150
    per_row, per_column = 2, 4
    row_count, col_count = 0, 0

    for ID, img_path in images:
        if row_count == per_row:
            row_count = 0
            col_count += 1
            if col_count == per_column:
                col_count = 0
                c.showPage()

        x = x_margin + (row_count * (img_display_width + x_space))
        y = height - y_margin - img_display_height - (col_count * (img_display_height + y_space))

        c.drawImage(img_path, x, y, width=img_display_width, height=img_display_height, preserveAspectRatio=True)
        c.drawString(x, y - 15, ID)
        row_count += 1

    c.save()

def excel_to_sdf(xlsx_file, sdf_file):
    try:
        df = pd.read_excel(xlsx_file)
        if not validate_excel_format(df):
            print("Error: Excel file format is incorrect. First column should be molecule code/ID and second column should be SMILES.")
            return

        writer = Chem.SDWriter(sdf_file)
        for i, row in df.iterrows():
            smiles = str(row.iloc[1])
            ID = str(row.iloc[0])
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                mol.SetProp('ID', ID)
                for col in df.columns[2:]:
                    if pd.notna(row[col]):
                        mol.SetProp(str(col), str(row[col]))
                writer.write(mol)
            else:
                print(f"Warning: SMILES '{smiles}' could not be converted to a molecule.")
        writer.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def sdf_to_excel(sdf_file, xlsx_file):
    try:
        suppl = Chem.SDMolSupplier(sdf_file)
        df_list = []
        for mol in suppl:
            if mol is not None:
                props = mol.GetPropsAsDict()
                ID = props.pop('ID', '')
                smiles = Chem.MolToSmiles(mol)
                row_data = {'ID': ID, 'SMILES': smiles, **props}
                df_list.append(pd.DataFrame([row_data]))
        df_combined = pd.concat(df_list, ignore_index=True)
        df_combined.to_excel(xlsx_file, index=False)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Convert between SDF and Excel formats and generate PDF of molecule structures')
    parser.add_argument('file', type=str, help='Input file with either .sdf or .xlsx extension')
    args = parser.parse_args()
    file_ext = os.path.splitext(args.file)[1]

    if file_ext == '.xlsx':
        output_file = os.path.splitext(args.file)[0] + '.sdf'
        excel_to_sdf(args.file, output_file)
        df = pd.read_excel(args.file)
        output_dir = 'molecule_images'
        output_dir = tempfile.mkdtemp()
        images = generate_molecule_images(df, output_dir)
        pdf_file = os.path.splitext(args.file)[0] + '.pdf'
        create_pdf(pdf_file, images)
    elif file_ext == '.sdf':
        output_file = os.path.splitext(args.file)[0] + '.xlsx'
        sdf_to_excel(args.file, output_file)
        df = pd.read_excel(output_file)
        output_dir = 'molecule_images'
        output_dir = tempfile.mkdtemp()
        images = generate_molecule_images(df, output_dir)
        pdf_file = os.path.splitext(args.file)[0] + '.pdf'
        create_pdf(pdf_file, images)

if __name__ == "__main__":
    main()