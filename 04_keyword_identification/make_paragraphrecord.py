import pandas as pd
from pathlib import Path
import argparse

def make_paragraphrecord(n_entries, filepath=None, save_df=True, return_df=False):
    div, mod = divmod(n_entries, 500)
    colnames = ['File Name','Starting Row','Ending Row','Name of RA']
    df = pd.DataFrame(columns=colnames)
    
    # create list of 1 to div
    list1 = [x + 1 for x in range(div+1)]
    # create list of 1, 501, ...
    list2 = [500 * x + 1 for x in range(div+1)]
    # create list of 500, 1000, ...
    list3 = [500 * (x + 1) for x in range(div+1)]
    if n_entries > 500:
        list3[-1] = list3[-2] + mod
    else:
        list3[-1] = mod
    
    df['File Name'] = list1
    df['Starting Row'] = list2
    df['Ending Row'] = list3
    df['Name of RA'] = ""
    
    if save_df == True:
        if filepath == None:
            print("filepath cannot be None if you are saving the df!")
            return
        df.to_excel(Path(filepath), index=False)
    if return_df == True:
        print(df)
        return df

# Tests
# df1 = make_paragraphrecord(21334, save_df=False, return_df=True)
# df2 = make_paragraphrecord(123, save_df=False, return_df=True)
# make_paragraphrecord(87654, r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\Paragraph Record\paragraphrecord_test.xlsx")
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='make paragraph_record')
    parser.add_argument('n_entries', help='total number of entries / paragraphs', type=int)
    parser.add_argument('-f', '--outputfilepath', help='.xlsx filepath for where you want to save the output (default paragraphrecord_fromterminal.xlsx)', default="paragraphrecord_fromterminal.xlsx")
    parser.add_argument('-s', '--save_df', help='whether to save the df (default True); True or False', default=True)
    parser.add_argument('-r', '--return_df', help='whether to return the df (default False); True or False', default=False)

    args = parser.parse_args()
    save_df =  False if args.save_df == "False" else True
    return_df = True if args.return_df == "True" else False
    make_paragraphrecord(args.n_entries, args.outputfilepath, save_df, return_df)


