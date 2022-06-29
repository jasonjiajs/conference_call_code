Steps:

- Record mouse clicks with record_mouse_clicks.py (to update to download_conference_calls_from_thomsonone.py, if necessary). Current mouse click co-ordinates assume that the screen resolution is 1920 x 1080 (pixels).

- Download conference calls with download_conference_calls_from_thomsonone.py

- Check that the .pdf and .xls files are in pairs with check_if_pdf_and_xls_are_in_pairs.py

- Combine xls files with combine_xls_files_and_save_as_xlsx.py to get xls_combined.xlsx.

- Scroll through the rows of xls_combined.xlsx, and check for any entries with "The application encountered an internal error.  Research: Unknown error". These happen when the xls file is not downloaded correctly, so find the corrupted xls file and redownload it from Thomson One. 

![image](https://user-images.githubusercontent.com/90637415/176491766-4d37069a-ec49-48ca-9291-5bb8c231fc9a.png)
