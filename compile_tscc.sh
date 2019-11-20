source ./module-reset.sh
cd $1
chmod +rx configSKIRT.sh 
chmod +rx makeSKIRT.sh 
CPATH=$(which gcc)
CPPPATH=$(which g++)
# Need to manually give SKIRT config the compiler paths since TSCC has issues getting the correct ones
./configSKIRT.sh BUILD_WITH_MPI=ON CMAKE_C_COMPILER=$CPATH CMAKE_CXX_COMPILER=$CPPPATH MPI_CXX_INCLUDE_PATH=$MPIHOME/include
./makeSKIRT.sh
