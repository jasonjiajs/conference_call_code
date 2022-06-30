#!/bin/bash

#----------------------------------
# Account Information

#SBATCH --account=pi-kilianhuber

#------------------------------
# Resources requested

#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=20G
#SBATCH --cores-per-socket=2
#SBATCH --time=5-00:00:00
#SBATCH --output=keywordident2.out

#---------------------
# Job specific name

#SBATCH --job-name=keywordident2

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

cd "/project/kh_mercury_1/CriCount"

srun python3 keyword_ident_2_mercury_sixun.py 
# /project/kh_mercury_1/WorkTemp/csv1 /project/kh_mercury_1/CriCount2/group1

