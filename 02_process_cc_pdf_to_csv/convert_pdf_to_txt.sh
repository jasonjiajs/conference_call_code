#!/bin/bash

#----------------------------------
# Account Information

#SBATCH --account=pi-kilianhuber
#SBATCH --mail-user=jason.jia@chicagobooth.edu

#------------------------------
# Resources requested

#SBATCH --partition=standard  # standard (default), long, gpu, mpi, highmem
#SBATCH --cpus-per-task=1     # number of CPUs requested (for parallel tasks)
#SBATCH --mem-per-cpu=2G     # requested memory
#SBATCH --time=1-00:00:00     # Time your job is allowed to run (d-hh:mm:ss)

#---------------------------------------------------------------------------------
# Job specific name (helps organize and track progress of jobs, optional parameters)
# '%A': array-job ID (e.g. 7823505)
# '%a': task ID (e.g. 1, 2, 3)
# '%J': job ID (e.g. 7823507, 7823506, 7823505)

#SBATCH --job-name=pdftotext
#SBATCH --output=out/pdftotext%A-%a-%J.out 

#-----------------------
# useful variables

echo "-------------------------------------------"
echo "Job ID: $SLURM_JOB_ID"
echo "Job User: $SLURM_JOB_USER"
echo "Num Cores: $SLURM_JOB_CPUS_PER_NODE"

#------------------------
# echo inputted command-line arguments

echo "-------------------------------------------"
echo "Input folder: $1"
echo "Output folder: $2"

#------------------------
# change directory to input folder

cd $1

#--------------------------
# for every pdf in the file, use pdftotext to tranfer to .txt files, and
# save to output folder

echo "-------------------------------------------"
echo "Converting .pdf to .txt:"

for f in *.pdf
do
	outputfilepath=$2"/${f%.*}.txt"
	echo $outputfilepath
	pdftotext -layout "$f" "$outputfilepath"
done

echo "-------------------------------------------"
echo "Done!"

#--------------------------
# Example command: sbatch convert_pdf_to_txt.sh /project/kh_mercury_1/conference_call/output/01_download_cc/01.1_pdf_20210101_20220617 /project/kh_mercury_1/conference_call/output/02_process_cc/02.1_txt_20210101_20220617

#--------------------------

# Below: The code to do it by running it directly on the terminal, without submitting a job via SLURM.

#--------------------------

# read -p "Input folder - download_cc/pdf (no quotation marks): " inputfolder
# read -p "Output folder - process_cc/txt (no quotation marks): " outputfolder

#--------------------------

# cd $inputfolder

#--------------------------

# for every pdf in the file, use pdftotext to tranfer to .txt files, and
# save to output folder

#for f in *.pdf
#do
#	outputfilepath=$outputfolder"/${f%.*}.txt"
#	echo $outputfilepath
#	pdftotext -layout "$f" "$outputfilepath"
#done
#echo done!