# SKIRT Test Run

This example downloads, compiles, and runs SKIRT.

First, download and compile SKIRT
```console
make compile
```

If there is an issue with the install clean up the directory first before retrying using
```console
make purge
```

Second, if you want to set up your own parameters for SKIRT build SKIRT using
```console
make build
```

Some preset SKIRT builds for FIRE snapshots are already provided in the sample folder. Sample_MW.ski is for MW like dust species, and Sample_SMC.ski is for SMC like dust species.

Edit the parameters in run.py to get data from the snapshot you want and what data you want to include. Then process your snapshot using
```console
make compile_data
```

Last, submit your SKIRT job using
```console
make submit
```

After SKIRT is finished running, all outputs can be found in the output directory.



