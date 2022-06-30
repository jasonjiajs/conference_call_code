Steps:
- Copy .pdf files from local drive to Mercury drive
- Add a new folder in /project/kh_mercury_1/conference_call/output/02_process_cc, with foldre name "02.1_txt_[pull_name]". This folder will contain the .txt files.
- Convert .pdf files to .txt files with pdftransfer.sh in Mercury.
- Copy .txt files from Mercury to local drive.
- Convert .txt files to .csv files with combine_xls_and_txt_and_save_as_csv.jl. Run the code in Atom.
