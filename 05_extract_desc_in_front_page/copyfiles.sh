#!/bin/bash

#----------------------------------
# Account Information

#SBATCH --account=pi-kilianhuber

#------------------------------
# Resources requested

#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=24G
#SBATCH --time=7-00:00:00
#SBATCH --output=copyfiles.out

#---------------------
# Job specific name

#SBATCH --job-name=copyfiles
#-----------------------
# useful variables

echo "Job ID: $SLURM_JOB_ID"
echo "Job User: $SLURM_JOB_USER"
echo "Num Cores: $SLURM_JOB_CPUS_PER_NODE"

#------------------------
# Load python

module load python/booth/3.8/3.8.5

#--------------------------
# run code

cd "/project/kh_mercury_1/ConferenceCallData/ListwithFrontPageDescription"

srun python3 copyfiles.py 

#--------------------------