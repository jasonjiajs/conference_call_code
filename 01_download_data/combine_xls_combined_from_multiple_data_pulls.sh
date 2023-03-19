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

#SBATCH --job-name=combine_xls_combined_from_multiple_data_pulls
#SBATCH --output=log/combine_xls_combined_from_multiple_data_pulls%A-%a-%J.out 

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
program_path="$1"
inputfilepath1="$2"
inputfilepath2="$3"
outputfilepath="$4"

echo "Program Path: $program_path"
echo "Input Filepath 1: $inputfilepath1"
echo "Input Filepath 2: $inputfilepath2"
echo "Output Filepath: $outputfilepath"
echo "-----------------------------------------------------------"

srun python3 $program_path $inputfilepath1 $inputfilepath2 $outputfilepath

echo "Done!"

# Example commands
# cd to /project/kh_mercury_1/conference_call/code/01_download_data first, i.e. folder containing the .py and .sh files.

# 20010101-20210909 (20010101-20210405 + 20201001-20210909)
# sbatch combine_xls_combined_from_multiple_data_pulls.sh combine_xls_combined_from_multiple_data_pulls.py /project/kh_mercury_1/conference_call/output/01_download_cc/01.2_xls_combined/single_data_pull/20010101-20210405/xls_combined_20010101-20210405.csv /project/kh_mercury_1/conference_call/output/01_download_cc/01.2_xls_combined/single_data_pull/20201001-20210909/xls_combined_20201001-20210909.csv /project/kh_mercury_1/conference_call/output/01_download_cc/01.2_xls_combined/multiple_data_pulls_combined/20010101-20210909/xls_combined_20010101-20210909.csv

# 20010101-20220617 (20010101-20210909 + 20210101-20220617)
# sbatch combine_xls_combined_from_multiple_data_pulls.sh combine_xls_combined_from_multiple_data_pulls.py /project/kh_mercury_1/conference_call/output/01_download_cc/01.2_xls_combined/multiple_data_pulls_combined/20010101-20210909/xls_combined_20010101-20210909.csv /project/kh_mercury_1/conference_call/output/01_download_cc/01.2_xls_combined/single_data_pull/20210101-20220617/xls_combined_20210101-20220617.csv /project/kh_mercury_1/conference_call/output/01_download_cc/01.2_xls_combined/multiple_data_pulls_combined/20010101-20220617/xls_combined_20010101-20220617.csv