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
#SBATCH --output=firmmatch1.out

#---------------------
# Job specific name

#SBATCH --job-name=firmmatch1
#-----------------------
# useful variables

echo "Job ID: $SLURM_JOB_ID"
echo "Job User: $SLURM_JOB_USER"
echo "Num Cores: $SLURM_JOB_CPUS_PER_NODE"

#-----------------------
# scratch space
scratch_dir="/scratch/${SLURM_JOB_USER}/${SLURM_JOB_ID}"
mkdir -p "$scratch_dir"
export TMPDIR="$scratch_dir"
export JOBLIB_TEMP_FOLDER="$scratch_dir"
#------------------------
# Load python

module load python/booth/3.6/3.6.12

#--------------------------
# run code

cd "/project/kh_mercury_1/FirmIdentification/FirmIdentFull"

srun python3 FirmIdentification.py 1

#--------------------------
# remove scratch
rm -r "$scratch_dir"