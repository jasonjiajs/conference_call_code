Steps:
- Identify paragraphs containing keywords with `identify_paragraphs_containing_keywords.ipynb`. The output is a .gzip file for each .csv file.
- Combine individual .gzip files with `combine_paragraph_gzip_files.py`. The output is a paragraphs_containing_keywords_combined.gzip file,
- Sort paragraphs_containing_keywords_combined.gzip and also convert it to entryfiles_combined with `sort_paragraphs_combined_and_convert_to_entryfiles_combined.ipynb`. The outputs are paragraphs_containing_keywords_combined_sorted.gzip and entryfilescombined.xlsx.
