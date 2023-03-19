Steps:

- Record mouse clicks with record_mouse_clicks.py (to update to download_conference_calls_from_thomsonone.py, if necessary). Current mouse click co-ordinates assume that the screen resolution is 1920 x 1080 (pixels).

- Download conference calls with download_conference_calls_from_thomsonone.py

- Check that the .pdf and .xls files are in pairs with check_if_pdf_and_xls_are_in_pairs.py

- Combine xls files with combine_xls_files.py to get xls_combined.xlsx (and xls_combined.csv).
  
  - If you want to combine the xls_combined files from different pulls, use combine_xls_combined_from_multiple_data_pulls.py.

- Scroll through the rows of xls_combined.xlsx, and check for any entries with "The application encountered an internal error.  Research: Unknown error". These happen when the xls file is not downloaded correctly, so find the corrupted xls file and redownload it from Thomson One. 

![image](https://user-images.githubusercontent.com/90637415/176491766-4d37069a-ec49-48ca-9291-5bb8c231fc9a.png)

- Get the titles (firm names) of each conference call, in every pdf, with get_titles_from_pdf.ipynb. This outputs pdf_titles.xlsx.

  - We note that the combined files (xls_combined.xlsx, pdf_titles.xlsx) are both in Excel, not in .csv. This is because some titles like "- EVENTS TRANSCRIPT ..." start with "-", and end up being interpreted as a non-existent formula (#NAME?) if read by Excel as a .csv. Saving as a .xlsx file solves this problem and makes it easier to do manual checks. Saving as .csv is good once you have done the checks because .xlsx files cannot store more than ~1M rows.

- The pdf_titles and xls_combined files record each conference call with the filestem (e.g. 20210101-20210104_1) and index (e.g. 0), giving an order to the list of calls (e.g. 0-th call in the pdf 20210101-20210104_1). We want to check that the i-th row in the pdf_titles and xls_combined files both record the same conference call, i.e. have the same filestem, index, and title (firm name). To do this, run check_if_pdf_and_xls_firm_names_are_the_same.ipynb. 

  - We note that the order of conference calls in Thomson One does not change with every query, unless new conference calls were added. Thus, if everything is correct, the sequences of conference calls in the pdf and xls files will match perfectly. This happens when all 3 tests pass.

  - Some pdf files only have 1 conference call. In this case, the title extracted may be different from that in the xls file, even though they both refer to the same firm. In these cases, check manually and update the "Manual Replacements" section of check_if_pdf_and_xls_firm_names_are_the_same.ipynb, so that tests will pass.

  - Tests could fail because a pdf file was downloaded twice in a glitch, once for the true filestem (e.g. 20210101-20210104_1), and once more for the next filestem (e.g. 20210101-20210104_2). On the other hand, the .xls file was correct for 20210101-20210104_2. Then the conference calls in 20210101-20210104_2.pdf will clash with that of 20210101-20210104_2.xls. 
