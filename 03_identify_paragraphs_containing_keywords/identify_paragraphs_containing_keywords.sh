#!/bin/bash

#---------------------------------------------------------------------------------
# Account information

#SBATCH --account=pi-kilianhuber              # basic (default), staff, phd, faculty

#---------------------------------------------------------------------------------
# Resources requested

#SBATCH --partition=standard       # standard (default), long, gpu, mpi, highmem
#SBATCH --cpus-per-task=1          # number of CPUs requested (for parallel tasks)
#SBATCH --mem-per-cpu=4G           # requested memory
#SBATCH --time=0-20:00:00          # wall closck limit (d-hh:mm:ss)

#---------------------------------------------------------------------------------
# Job specific name (helps organize and track progress of jobs)

#SBATCH --job-name=DS_2015  # user-defined job name

#---------------------------------------------------------------------------------
# Print some useful variables

echo "Job ID: $SLURM_JOB_ID"
echo "Job User: $SLURM_JOB_USER"
echo "Num Cores: $SLURM_JOB_CPUS_PER_NODE"

#---------------------------------------------------------------------------------
# Load necessary modules for the job

module load python/booth/3.6/3.6.12
source /project/kh_mercury_1/conference_call/code/env/bin/activate

#---------------------------------------------------------------------------------
# echo inputted command-line arguments

echo "Input folder: $1"
echo "Output folder: $2"
printf "\n"

#------------------------
# Commands to execute below...

srun python3 "CC_identify_keywords.py" "$SLURM_ARRAY_TASK_ID"