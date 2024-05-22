#!/bin/bash
#SBATCH -J SKIRT            # Job name
#SBATCH -o out.o            # Name of stdout output file
#SBATCH -e out.e            # Name of stderr error file
#SBATCH -p general          # Queue (partition) name
#SBATCH --nodes=1           # Total # of nodes 
#SBATCH --ntasks-per-node=4 # Total number of mpi tasks per node
#SBATCH --cpus-per-task=8   # number of cpus per mpi task = OMP_NUM_THREADS.
#SBATCH --mem=50G           # Total RAM to be used by this job
#SBATCH -t 01:00:00         # Run time (hh:mm:ss)
#SBATCH --mail-type=all     # Send email at begin and end of job
#SBATCH -A r00380           # Project/Allocation name
#SBATCH --mail-user=EMAIL   # Email to send all jobs alters to
#SBATCH -D .

# Note that there are a total of 128 cores per node so (ntasks-per-node) * (cpus-per-task) should always be less than or equal to 128.
# Also the max RAM is 256 GB.

export OMP_NUM_THREADS=4
date
module list

# Make a new folder for the output and copy all the files SKIRT uses into it
mkdir output
cp out.ski ./output/
cp star.dat ./output/
cp gas.dat ./output/
cd output
pwd

# Print out the SLURM info
echo $SLURM_JOB_NUM_NODES
echo $SLURM_NTASKS_PER_NODE
echo $SLURM_CPUS_PER_TASK


# Run with (ntasks-per-node) tasks each with (cpus-per-task) cores. 
# skirt is a little odd in that you need to give the number of cores/threads using the -t argument to skirt and not to srun
srun --ntasks-per-node=$SLURM_NTASKS_PER_NODE skirt -t $SLURM_CPUS_PER_TASK out.ski
date
exit
