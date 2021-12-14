#!/bin/bash

#---------------------------------------------------------------------------------
# Account information

#SBATCH --account=pi-kilianhuber              # basic (default), staff, phd, faculty

#---------------------------------------------------------------------------------
# Resources requested

#SBATCH --partition=highmem       # standard (default), long, gpu, mpi, highmem
#SBATCH --cpus-per-task=16          # number of CPUs requested (for parallel tasks)
#SBATCH --mem-per-cpu=16G           # requested memory
#SBATCH --time=1-20:00:00          # wall closck limit (d-hh:mm:ss)

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

#---------------------------------------------------------------------------------
# Commands to execute below...

srun python3 "nameMatching.py" "$SLURM_ARRAY_TASK_ID"