#!/bin/bash

#----------------------------------
# Account Information

#SBATCH --account=pi-kilianhuber

#------------------------------
# Resources requested

#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=32G
#SBATCH --cores-per-socket=2
#SBATCH --time=0-10:00:00

#---------------------
# Job specific name

#SBATCH --job-name=confcallpdftotext

#-----------------------
# useful variables

echo "Job ID: $SLURM_JOB_ID"
echo "Job User: $SLURM_JOB_USER"
echo "Num Cores: $SLURM_JOB_CPUS_PER_NODE"
printf "\n"

#------------------------
# echo inputted command-line arguments

echo "Input folder: $1"
echo "Output folder: $2"
printf "\n"

#------------------------
# change directory to input folder

cd $1

#--------------------------
# for every pdf in the file, use pdftotext to tranfer to .txt files, and
# save to output folder

for f in *.pdf
do
	outputfilepath=$2"/${f%.*}.txt"
	echo $outputfilepath
	pdftotext -layout "$f" "$outputfilepath"
done
echo done!

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