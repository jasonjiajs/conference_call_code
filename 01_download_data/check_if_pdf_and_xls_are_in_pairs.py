# Import Packages
import os, sys
from pathlib import Path

# Example command:
# python check_if_pdf_and_xls_are_in_pairs.py C:\Users\jasonjia\Dropbox\Projects\conference_call\output\01_download_cc\01.1_pdf_20210101_20220617 C:\Users\jasonjia\Dropbox\Projects\conference_call\output\01_download_cc\01.1_xls_20210101_20220617

# Folder locations
pdf_folder = Path(sys.argv[1])
xls_folder = Path(sys.argv[2])
print("pdf folder:", pdf_folder)
print("xls folder:", xls_folder)

# Function: for each file in folder A, check if an equivalent file in folder B (same filestem, but with extension B) exists.
def check_pairs(folder_A, folder_B, extension_B):
    for item in folder_A.iterdir():
        filestem = item.stem
    filename_B = filestem + extension_B
    filepath_B = Path(folder_B / filename_B)
    if not(os.path.exists(filepath_B)):
        print("File missing:", filename_B)

# For each file in .pdf, check if an equivalent .xls file exists
print("\n--- For each file in .pdf, checking if an equivalent .xls file exists ---")
check_pairs(pdf_folder, xls_folder, ".xls")

# For each file in .xls, check if an equivalent .pdf file exists
print("\n--- For each file in .xls, checking if an equivalent .pdf file exists ---")
check_pairs(xls_folder, pdf_folder, ".pdf")

print("\n--- Done! ---")