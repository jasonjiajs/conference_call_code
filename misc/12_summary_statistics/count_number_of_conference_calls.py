import pandas as pd
from pathlib import Path

xlsfolder = Path(r"/project/kh_mercury_1/conference_call/output/01_download_cc/01.1_xls_1")
report_id_compiled_outputfilepath = Path(r"/project/kh_mercury_1/conference_call/output/12_summary_statistics/report_id_01.1_xls_1.csv")
xls_compiled_outputfilepath = Path(r"/project/kh_mercury_1/conference_call/output/12_summary_statistics/xls_compiled_01.1_xls_1.csv")

df_report_id_compiled = pd.DataFrame()

def compile_xls(xlsfolder, compile_all_cols=False):
    
    df_xls_compiled = pd.DataFrame()

    # For each xls file, read and get a list of the report IDs (by default, unless you specify all cols), 
    # then save it as a csv file
    for xlsfile in xlsfolder.iterdir():
        if xlsfile.suffix == '.xls':
            print(xlsfile)

            try:
                if compile_all_cols == False:
                    df_xls = pd.read_html(str(xlsfile))[0]['Report #']
                else:
                    df_xls = pd.read_html(str(xlsfile))[0]

                if df_xls_compiled.shape[0] == 0:
                    df_xls_compiled = df_xls
                else:
                    df_xls_compiled = df_xls_compiled.append(df_xls)

                print(df_xls_compiled.shape)
            except:
                print("Error reading 'Report #' column - check xls file!")
                
    return df_xls_compiled

df_report_id_compiled = compile_xls(xlsfolder)
df_xls_compiled = compile_xls(xlsfolder, compile_all_cols = True)

df_report_id_compiled.to_csv(report_id_compiled_outputfilepath, index = None)
df_xls_compiled.to_csv(xls_compiled_outputfilepath, index = None)