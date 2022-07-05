Steps:
- Check for updates to the Compustat (actually capitalIQ) and Hassan files and download them.
- Process the Hassan file with `process_hassan.py`.
- Convert the Compustat files to .csv with `convert_compustat_sas7bdat_to_csv.py`.
  - Note: this warning may arise, but it won't affect the csv: [ciqcompany.sas7bdat] header length 65536 != 8192
- Merge and process the Compustat files with `merge_and_process_compustat.py`.
- Combine the processed Hassan and Compustat files with `combine_processed_hassan_and_compustat_files.py`.
- Get firm names to match from entryfiles using `get_firm_names_to_match_from_entryfiles.ipynb`. The outputs are: entryfilescombined_with_cleanfirmnames.xlsx, and cleanfirmnames_to_match.xlsx. 
  - Note that the same function is used to clean firm names (get_clean_firm_name) for both the source files (Hassan and Compustat), as well as the target files (entryfilescombined).
  - Developing the function first used entries from entryfilescombined, then was modified based on entries from Hassan and Compustat.
