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
#SBATCH --output=keywordident1_5.out

#---------------------
# Job specific name

#SBATCH --job-name=keywordident1_5
#-----------------------
# useful variables

echo "Job ID: $SLURM_JOB_ID"
echo "Job User: $SLURM_JOB_USER"
echo "Num Cores: $SLURM_JOB_CPUS_PER_NODE"

#------------------------
# Load python

module load python/booth/3.6/3.6.12

#--------------------------
# run code

cd "/project/kh_mercury_1/CriCount"

srun python3 keyword_ident_1_mercury_sixun_5.py 
# srun python3 keyword_ident_1_mercury.py 1

#--------------------------