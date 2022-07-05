Steps:
- Get firm names to match from entryfiles using `get_firm_names_to_match_from_entryfiles.ipynb`. The outputs are: entryfilescombined_with_cleanfirmnames.xlsx, and cleanfirmnames_to_match.xlsx. 
- Check for updates to the Compustat (actually capitalIQ) and Hassan files and download them.
- Process the Hassan file with `process_hassan.py`.
- Convert the Compustat files to .csv with `convert_compustat_sas7bdat_to_csv.py`.
  - Note: this warning may arise, but it won't affect the csv: [ciqcompany.sas7bdat] header length 65536 != 8192
