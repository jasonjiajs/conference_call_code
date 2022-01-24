import pandas as pd
from pathlib import Path

xlsfolder = Path(r"/project/kh_mercury_1/conference_call/output/01_download_cc/01.1_xls_1")
outputfilepath = Path(r"/project/kh_mercury_1/conference_call/output/12_summary_statistics/report_id_01.1_xls_1.csv")

df_report_id_compiled = pd.DataFrame()

# For each xls file, read and get a list of the report IDs, then save it as a csv file
for xlsfile in xlsfolder.iterdir():
    if xlsfile.suffix == '.xls':
        print(xlsfile)
        try:
            df_report_id = pd.read_html(str(xlsfile))[0]['Report #']
            if df_report_id_compiled.shape[0] == 0:
                df_report_id_compiled = df_report_id
            else:
                df_report_id_compiled = df_report_id_compiled.append(df_report_id)
                print(df_report_id_compiled.shape)
        except:
            print("Error reading 'Report #' column - check xls file!")
        

df_report_id_compiled.to_csv(outputfilepath, index = None)