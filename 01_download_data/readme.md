Steps:

- Record mouse clicks with record_mouse_clicks.py (to update to download_conference_calls_from_thomsonone.py, if necessary). Current mouse click co-ordinates assume that the screen resolution is 1920 x 1080 (pixels).

- Download conference calls with download_conference_calls_from_thomsonone.py

- Check that the .pdf and .xls files are in pairs with check_if_pdf_and_xls_are_in_pairs.py

- Combine xls files with combine_xls_files_and_save_as_xlsx.py to get xls_combined.xlsx.

- Scroll through the rows of xls_combined.xlsx, and check for any entries with "The application encountered an internal error.  Research: Unknown error". These happen when the xls file is not downloaded correctly, so find the corrupted xls file and redownload it from Thomson One. 

![image](https://user-images.githubusercontent.com/90637415/176491766-4d37069a-ec49-48ca-9291-5bb8c231fc9a.png)

- Get the titles (firm names) of each conference call, in every pdf, with get_titles_from_pdf.ipynb. However, this code will not generate correct results for pdfs containing only 1 conference call. We will check this in the next step.

- The pdf_titles and xls_combined files record each conference call with the filestem (e.g. 20210101-20210104_1) and index (e.g. 0), giving an order to the list of calls (e.g. 0-th call in the pdf 20210101-20210104_1). We want to check that the i-th row in the pdf_titles and xls_combined files both record the same conference call, i.e. have the same filestem, index, and title (firm name). To do this, run check_if_pdf_and_xls_firm_names_are_the_same.ipynb.

If you see something like the following, where the titles are not firm names but page numbers, you've hit an edge case where the pdf only contains 1 conference call. Resolve this by editing the pdf_titles.csv file manually, and rerun.

![image](https://user-images.githubusercontent.com/90637415/176561880-92c7d4cf-93d0-4106-86ce-5925fdbd2948.png)
