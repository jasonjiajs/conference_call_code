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
# Job specific name (helps organize and track progress of jobs)

#SBATCH --job-name=read_arg # user-defined job name
#SBATCH -o out/slurm-%j.out # location and name of out file

#---------------------------------------------------------------------------------
# Email settings

#SBATCH --mail-type=END,FAIL     # mail events (can use any combination of the following: ALL, NONE, BEGIN, END, FAIL)
#SBATCH --mail-user=jason.jia@chicagobooth.edu 

#-----------------------
# useful variables

echo "Job ID: $SLURM_JOB_ID"
echo "Job User: $SLURM_JOB_USER"
echo "Num Cores: $SLURM_JOB_CPUS_PER_NODE"
printf "\n"

#------------------------
# Load python

module load python/booth/3.6/3.6.12

#--------------------------
# echo inputted command-line arguments

echo "Argument 1 (SLURM): $1"
echo "Argument 2 (SLURM): $2"
printf "\n"

#--------------------------
# pass command-line arguments inputted on SLURM as command-line arguments 
# for the python file

srun python3 read_arg.py $1 $2

# expect .py file to print out:
# "Argument 1 (Python): $1"
# "Argument 2 (Python): $2"
# "Arguments successfully passed from: SLURM command line -> .sh script -> Python command line -> .py script!""

#--------------------------
# print information about completed job

echo done!
printf "\n"
sacct -j $SLURM_JOB_ID --format=MaxRSS,elapsed,reqmem,timelimit