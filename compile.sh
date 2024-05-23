source ./activate.sh
cd $1
# Make scripts executable
chmod +rx configSKIRT.sh 
chmod +rx makeSKIRT.sh 

./configSKIRT.sh BUILD_WITH_MPI=ON
./makeSKIRT.sh
