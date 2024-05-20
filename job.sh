#!/bin/bash
#SBATCH -J SKIRT          # Job name
#SBATCH -o out.o           # Name of stdout output file
#SBATCH -e out.e           # Name of stderr error file
#SBATCH -p normal          # Queue (partition) name
#SBATCH -N 1              # Total # of nodes 
#SBATCH --ntasks-per-node=32             # Total # of mpi tasks per node = # of Cores per Node (128) / OMP_NUM_THREADS
#SBATCH --cpus-per-task=4  # of cpus per mpi task = OMP_NUM_THREADS
#SBATCH -t 02:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-type=all    # Send email at begin and end of job
#SBATCH -A AST21010        # Project/Allocation name (req'd if you have more than 1)
#SBATCH --mail-user=EMAIL
#SBATCH -D .
#SBATCH --dependency=


pwd
date
source ./activate.sh
cd output
# Run with 6 task each with 6 cores. 
ibrun -cpus-per-task=$SLURM_CPUS_PER_TASK --ntasks-per-node=$SLURM_NTASKS_PER_NODE --nodes=$SLURM_JOB_NUM_NODES -m -v skirt out.ski
date
exit
