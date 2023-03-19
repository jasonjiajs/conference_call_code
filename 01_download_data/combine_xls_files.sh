#!/bin/bash

#---------------------------------------------------------------------------------
# Account information

#SBATCH --account=pi-kilianhuber # account you belong to 
#SBATCH --mail-user=jason.jia@chicagobooth.edu

#---------------------------------------------------------------------------------
# Resources requested (recommended parameters to specify)

#SBATCH --partition=standard  # standard (default), long, gpu, mpi, highmem
#SBATCH --cpus-per-task=1     # number of CPUs requested (for parallel tasks)
#SBATCH --mem-per-cpu=16G     # requested memory
#SBATCH --time=1-00:00:00     # Time your job is allowed to run (d-hh:mm:ss)

#---------------------------------------------------------------------------------
# Array information

# #SBATCH --array=1-16

#---------------------------------------------------------------------------------
# Job specific name (helps organize and track progress of jobs, optional parameters)
# '%A': array-job ID (e.g. 7823505)
# '%a': task ID (e.g. 1, 2, 3)
# '%J': job ID (e.g. 7823507, 7823506, 7823505)

#SBATCH --job-name=combine_xls_files
#SBATCH --output=log/combine_xls_files%A-%a-%J.out 

#---------------------------------------------------------------------------------
# Print some useful variables

echo "-----------------------------------------------------------"
echo "Output from Shell Script:"
echo "Job ID: $SLURM_JOB_ID"
echo "Job User: $SLURM_JOB_USER"
echo "Num Cores: $SLURM_JOB_CPUS_PER_NODE"
echo "Array(Task ID): $SLURM_ARRAY_TASK_ID of $SLURM_ARRAY_TASK_COUNT"

#---------------------------------------------------------------------------------
# Load necessary modules for the job

module load python/booth/3.8

# Go into env
# source /home/jasonjia/standard_env_jason/bin/activate

#---------------------------------------------------------------------------------
# Commands to execute below...
program_path="$1" # i.e. combine_xls_files.py
input_folder="$2"
output_filepath="$3"

echo "Program Path: $program_path"
echo "Input Folder: $input_folder"
echo "Output Filepath: $output_filepath"
echo "-----------------------------------------------------------"

srun python3 $program_path $input_folder $output_filepath

echo "Done!"

# Example commands
# cd to /project/kh_mercury_1/conference_call/code/01_download_data first, i.e. folder containing the .py and .sh files.
# sbatch combine_xls_files.sh combine_xls_files.py /project/kh_mercury_1/conference_call/output/01_download_cc/01.1_xls/20010101-20210405 /project/kh_mercury_1/conference_call/output/01_download_cc/01.2_xls_combined/single_data_pull/20010101-20210405/xls_compiled_20010101-20210405.csv
