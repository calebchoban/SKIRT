module purge
module load cmake
export MODULEPATH="/projects/builder-group/jpg/modulefiles/compilers:${MODULEPATH}"
module load gnu/7.1.0 openmpi_ib
module list
export PATH="${PWD}/release/SKIRT/main:${PATH}"
