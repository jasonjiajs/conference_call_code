# Conference Call Code

- This folder contains all codes and documentation for the conference call project. 
- It is cloned into both Dropbox (your work laptop) and Mercury under .../conference_call/code, 
so the two folders are identical as long as commits, pushes and pull requests are made regularly.
- The input is a date range, e.g. 20200101-20201231. The main output is a df of paragraphs from all Refinitiv transcripts within the date range (saved as "entry files"), where each paragraph contains some keyword of interest. The df also contains identifiers for the conference call (e.g. title, date, report ID), firm name, gvkey and HQ country.
- The main pipeline is split into 5 stages, `01` to `05`, in order. Additional tasks (usually one-off) are in `one_off`.

To dos:
- The folder structure and folder names were standardized after all codes were run, so the folder and file paths in some code files will need to be updated as well.
- The env folders contain some data for the Python environment in Mercury. This is not yet synchronized. We should replace this folder with a file containing all the packages required instead, and any user can just load the env using that requirements file.
