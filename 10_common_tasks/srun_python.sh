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

#SBATCH --job-name=srun_python  # user-defined job name
#SBATCH -o out/slurm-%j.out # STDOUT

#---------------------------------------------------------------------------------
# Email settings

#SBATCH --mail-type=END,FAIL     # Mail events (can use any combination of the following: ALL, NONE, BEGIN, END, FAIL)
#SBATCH --mail-user=jason.jia@chicagobooth.edu

#---------------------------------------------------------------------------------
# Print some useful variables

echo "Job ID: $SLURM_JOB_ID"
echo "Job User: $SLURM_JOB_USER"
echo "Num Cores: $SLURM_JOB_CPUS_PER_NODE"
printf "\n"

#---------------------------------------------------------------------------------
# Load necessary modules for the job

module load python/booth/3.6/3.6.12

#---------------------------------------------------------------------------------
# Go into env
source /project/kh_mercury_1/conference_call/code/env/bin/activate

#--------------------------
# echo inputted command-line arguments

echo "Python file to run: $1"
printf "\n"

#---------------------------------------------------------------------------------
# Commands to execute below...

srun python3 $1

#--------------------------
# print information about completed job

echo $1: done!
printf "\n"
sacct -j $SLURM_JOB_ID --format=MaxRSS,elapsed,reqmem,timelimit